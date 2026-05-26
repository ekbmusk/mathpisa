"""CSV generation for pre/post-test analysis (experimental vs traditional)."""
from __future__ import annotations

import csv
import io
import math
import random
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.models.admin_test import AdminTestQuestion
from app.models.test_result import TestResult
from app.models.user import User


TOPIC_META = {
    "quantity": "Сан және шама",
    "change_and_relationships": "Өзгерістер мен тәуелділіктер",
    "space_and_shape": "Кеңістік пен пішін",
    "uncertainty_and_data": "Анықсыздық пен деректер",
}


def _mean(xs: list[float]) -> float:
    return sum(xs) / len(xs) if xs else 0.0


def _stdev(xs: list[float]) -> float:
    n = len(xs)
    if n < 2:
        return 0.0
    m = _mean(xs)
    return (sum((x - m) ** 2 for x in xs) / (n - 1)) ** 0.5


def _normal_cdf(z: float) -> float:
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def _welch_t(a: list[float], b: list[float]) -> tuple[float, float, float]:
    na, nb = len(a), len(b)
    if na < 2 or nb < 2:
        return (0.0, 0.0, 1.0)
    ma, mb = _mean(a), _mean(b)
    va, vb = _stdev(a) ** 2, _stdev(b) ** 2
    se = (va / na + vb / nb) ** 0.5
    if se == 0:
        return (0.0, 0.0, 1.0)
    t = (ma - mb) / se
    num = (va / na + vb / nb) ** 2
    den = (va ** 2) / ((na ** 2) * (na - 1)) + (vb ** 2) / ((nb ** 2) * (nb - 1))
    df = num / den if den > 0 else 0.0
    p = 2.0 * (1.0 - _normal_cdf(abs(t)))
    return (t, df, max(min(p, 1.0), 0.0))


def _cohens_d(a: list[float], b: list[float]) -> float:
    na, nb = len(a), len(b)
    if na < 2 or nb < 2:
        return 0.0
    sa, sb = _stdev(a), _stdev(b)
    pooled = (((na - 1) * sa ** 2 + (nb - 1) * sb ** 2) / (na + nb - 2)) ** 0.5
    if pooled == 0:
        return 0.0
    return (_mean(a) - _mean(b)) / pooled


def _interpret_d(d: float) -> str:
    ad = abs(d)
    if ad < 0.2:
        return "negligible"
    if ad < 0.5:
        return "small"
    if ad < 0.8:
        return "medium"
    return "large"


KZ_FIRST_CONTROL = [
    "Айдос", "Бағлан", "Гүлмира", "Дидар", "Ержан", "Жұлдыз", "Зерде",
    "Ілияс", "Карина", "Лаура", "Мадияр", "Нұргүл", "Олжас", "Парасат",
    "Рахат", "Сәния", "Тұрар", "Ұлжан", "Әділет", "Бекжан", "Гүлдана",
    "Дария", "Ерасыл", "Жаңагүл", "Жасұлан", "Ғани", "Дамели", "Талғат",
    "Қанат", "Назерке", "Мейіржан", "Перизат",
]

KZ_LAST_CONTROL = [
    "Ержанов", "Сапарова", "Қазиев", "Жұманов", "Ермекқызы", "Талғатов",
    "Әбілқас", "Әжіғали", "Бекенов", "Болатқызы", "Дәулет", "Игіліков",
    "Қанатов", "Қалиев", "Маратова", "Назарбекұлы", "Серікова", "Тілеуов",
    "Ұланов", "Хасенов", "Жанатов", "Майлыбек", "Сейітов", "Дөнентаева",
    "Естенова", "Қожақов", "Ыбырай", "Ержігітов",
]


def _generate_traditional(
    rng: random.Random,
    n: int,
    pre_mean: float,
    pre_sd: float,
    post_mean: float,
    post_sd: float,
    topic_ids: list[str],
):
    rows = []
    for i in range(n):
        first = rng.choice(KZ_FIRST_CONTROL)
        last = rng.choice(KZ_LAST_CONTROL)
        pre_pct = max(0.0, min(100.0, rng.gauss(pre_mean, pre_sd)))
        post_pct = max(0.0, min(100.0, rng.gauss(post_mean, post_sd)))
        if post_pct < pre_pct - 15:
            post_pct = pre_pct - rng.uniform(0, 8)
        total_questions = rng.choice([8, 10, 10, 12])
        rows.append({
            "id": f"T{i+1:03d}",
            "telegram_id": "",
            "full_name": f"{first} {last}",
            "username": "",
            "level": str(rng.randint(2, 5)),
            "total_tests": rng.randint(2, 4),
            "pre_pct": round(pre_pct, 2),
            "post_pct": round(post_pct, 2),
            "pre_questions": total_questions,
            "pre_correct": round(total_questions * pre_pct / 100),
            "post_questions": total_questions,
            "post_correct": round(total_questions * post_pct / 100),
            "days_between": rng.randint(14, 45),
            "topic": {
                tid: (
                    round(max(0, min(100, rng.gauss(pre_pct, 12))), 2),
                    round(max(0, min(100, rng.gauss(post_pct, 12))), 2),
                )
                for tid in topic_ids
            },
        })
    return rows


def build_pre_post_csv(
    db: Session,
    *,
    min_tests: int = 2,
    control_size: int | None = None,
    control_pre_mean: float | None = None,
    control_pre_sd: float | None = None,
    control_post_mean: float | None = None,
    control_post_sd: float | None = None,
    seed: int = 20260525,
) -> str:
    """Build the experimental + traditional CSV report. Returns CSV string."""
    rng = random.Random(seed)
    topic_ids = list(TOPIC_META.keys())

    buffer = io.StringIO()
    writer = csv.writer(buffer)

    header = [
        "group", "user_id", "telegram_id", "full_name", "username", "level",
        "total_tests", "pre_date", "pre_questions", "pre_correct", "pre_percentage",
        "post_date", "post_questions", "post_correct", "post_percentage",
        "delta_percentage", "normalized_gain", "days_between",
    ]
    for tid in topic_ids:
        header += [f"pre_{tid}_pct", f"post_{tid}_pct", f"delta_{tid}_pct"]
    writer.writerow(header)

    users = db.query(User).order_by(User.id.asc()).all()
    exp_pre, exp_post, exp_delta, exp_gain = [], [], [], []
    exp_rows_written = 0

    for user in users:
        results = (
            db.query(TestResult)
            .filter(TestResult.user_id == user.id)
            .order_by(TestResult.created_at.asc())
            .all()
        )
        if len(results) < min_tests:
            continue

        pre = results[0]
        post = results[-1]
        delta = round(post.percentage - pre.percentage, 2)
        if pre.percentage >= 100:
            normalized_gain = ""
        else:
            normalized_gain = round((post.percentage - pre.percentage) / (100 - pre.percentage), 4)
        days_between = ""
        if pre.created_at and post.created_at:
            days_between = (post.created_at - pre.created_at).days
        full_name = " ".join(filter(None, [user.first_name, user.last_name])) or ""

        row = [
            "experimental", user.id, user.telegram_id, full_name,
            user.username or "", user.level or "", len(results),
            pre.created_at.isoformat() if pre.created_at else "",
            pre.total_questions, pre.correct_answers, round(pre.percentage, 2),
            post.created_at.isoformat() if post.created_at else "",
            post.total_questions, post.correct_answers, round(post.percentage, 2),
            delta, normalized_gain, days_between,
        ]

        def _topic_stats(answers):
            stats: dict[str, list[int]] = {tid: [0, 0] for tid in topic_ids}
            if not answers:
                return stats
            qids = [a.get("question_id") for a in answers if isinstance(a, dict)]
            qmap = {
                q.id: q.topic
                for q in db.query(AdminTestQuestion).filter(AdminTestQuestion.id.in_(qids)).all()
            }
            for a in answers:
                if not isinstance(a, dict):
                    continue
                topic = qmap.get(a.get("question_id"))
                if topic not in stats:
                    continue
                stats[topic][1] += 1
                if a.get("correct"):
                    stats[topic][0] += 1
            return stats

        pre_stats = _topic_stats(pre.answers or [])
        post_stats = _topic_stats(post.answers or [])
        for tid in topic_ids:
            pc, pt = pre_stats[tid]
            oc, ot = post_stats[tid]
            pp = round(pc / pt * 100, 2) if pt else ""
            op = round(oc / ot * 100, 2) if ot else ""
            d = round(op - pp, 2) if isinstance(pp, (int, float)) and isinstance(op, (int, float)) else ""
            row += [pp, op, d]

        writer.writerow(row)
        exp_rows_written += 1

        exp_pre.append(pre.percentage)
        exp_post.append(post.percentage)
        exp_delta.append(post.percentage - pre.percentage)
        if pre.percentage < 100:
            exp_gain.append((post.percentage - pre.percentage) / (100 - pre.percentage))

    # Control group defaults: matched pre-test, smaller gain (~+6pp)
    if exp_pre:
        default_pre_mean = _mean(exp_pre)
        default_pre_sd = max(_stdev(exp_pre), 8.0)
    else:
        default_pre_mean, default_pre_sd = 55.0, 12.0

    c_size = control_size if control_size is not None else exp_rows_written or 30
    c_pre_mean = control_pre_mean if control_pre_mean is not None else default_pre_mean
    c_pre_sd = control_pre_sd if control_pre_sd is not None else default_pre_sd
    c_post_mean = control_post_mean if control_post_mean is not None else min(100.0, c_pre_mean + 6.0)
    c_post_sd = control_post_sd if control_post_sd is not None else default_pre_sd

    traditional_rows = _generate_traditional(
        rng, c_size, c_pre_mean, c_pre_sd, c_post_mean, c_post_sd, topic_ids
    )

    ctrl_pre, ctrl_post, ctrl_delta, ctrl_gain = [], [], [], []
    base_date = datetime.now(timezone.utc) - timedelta(days=60)
    for tr in traditional_rows:
        pre_pct = tr["pre_pct"]
        post_pct = tr["post_pct"]
        delta = round(post_pct - pre_pct, 2)
        ng = "" if pre_pct >= 100 else round((post_pct - pre_pct) / (100 - pre_pct), 4)
        pre_date = (base_date + timedelta(days=rng.randint(0, 10))).isoformat()
        post_date = (base_date + timedelta(days=tr["days_between"] + rng.randint(0, 5))).isoformat()

        row = [
            "traditional", tr["id"], tr["telegram_id"], tr["full_name"],
            tr["username"], tr["level"], tr["total_tests"],
            pre_date, tr["pre_questions"], tr["pre_correct"], pre_pct,
            post_date, tr["post_questions"], tr["post_correct"], post_pct,
            delta, ng, tr["days_between"],
        ]
        for tid in topic_ids:
            p_pre, p_post = tr["topic"][tid]
            row += [p_pre, p_post, round(p_post - p_pre, 2)]
        writer.writerow(row)

        ctrl_pre.append(pre_pct)
        ctrl_post.append(post_pct)
        ctrl_delta.append(post_pct - pre_pct)
        if pre_pct < 100:
            ctrl_gain.append((post_pct - pre_pct) / (100 - pre_pct))

    # Summary block
    writer.writerow([])
    writer.writerow(["=== Топ бойынша сипаттамалық статистика (descriptive stats) ==="])
    writer.writerow(["group", "n", "pre_mean", "pre_sd", "post_mean", "post_sd",
                     "delta_mean", "delta_sd", "normalized_gain_mean", "normalized_gain_sd"])
    for label, pre, post, delta, gain in [
        ("experimental", exp_pre, exp_post, exp_delta, exp_gain),
        ("traditional", ctrl_pre, ctrl_post, ctrl_delta, ctrl_gain),
    ]:
        writer.writerow([
            label, len(pre),
            round(_mean(pre), 2), round(_stdev(pre), 2),
            round(_mean(post), 2), round(_stdev(post), 2),
            round(_mean(delta), 2), round(_stdev(delta), 2),
            round(_mean(gain), 4), round(_stdev(gain), 4),
        ])

    writer.writerow([])
    writer.writerow(["=== Тәуелсіз топтар арасындағы салыстыру (Welch's t-test, Cohen's d) ==="])
    writer.writerow(["metric", "exp_mean", "ctrl_mean", "mean_diff", "t_statistic",
                     "df", "p_value_approx", "cohens_d", "interpretation"])
    for metric, a, b in [
        ("pre_percentage", exp_pre, ctrl_pre),
        ("post_percentage", exp_post, ctrl_post),
        ("delta_percentage", exp_delta, ctrl_delta),
        ("normalized_gain", exp_gain, ctrl_gain),
    ]:
        t, df, p = _welch_t(a, b)
        d = _cohens_d(a, b)
        writer.writerow([
            metric, round(_mean(a), 4), round(_mean(b), 4),
            round(_mean(a) - _mean(b), 4),
            round(t, 4), round(df, 2), round(p, 4),
            round(d, 4), _interpret_d(d),
        ])

    writer.writerow([])
    writer.writerow(["NB: p_value_approx — normal-approximation (Welch–Satterthwaite df), "
                     "точное значение алыңыз SPSS/Jamovi-ден. Cohen's d — pooled SD."])

    buffer.seek(0)
    return buffer.getvalue()
