import { useState, useEffect, useRef, useCallback } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import WebApp from '@twa-dev/sdk'
import confetti from 'canvas-confetti'
import { Trophy, RotateCcw, Home, ChevronRight, Lightbulb, BookOpen, Shuffle, Zap, Sigma, TrendingUp, Shapes, PieChart } from 'lucide-react'
import TopBar from '../components/TopBar'
import ProgressBar from '../components/ProgressBar'
import Button from '../components/Button'
import { SkeletonCard } from '../components/SkeletonLoader'
import FormulaRenderer from '../components/FormulaRenderer'
import QuestionMedia from '../components/QuestionMedia'
import XPAnimation from '../components/XPAnimation'
import { testsAPI } from '../api/tests'
import { useUserStore } from '../store/userStore'

const TIMER = 40

const TOPIC_ICONS = {
  quantity: '🔢',
  change_and_relationships: '📈',
  space_and_shape: '📐',
  uncertainty_and_data: '📊',
}

const TOPIC_LUCIDE_ICONS = {
  quantity: Sigma,
  change_and_relationships: TrendingUp,
  space_and_shape: Shapes,
  uncertainty_and_data: PieChart,
}

function TimerCircle({ seconds }) {
  const r = 20, c = 2 * Math.PI * r
  const color = seconds <= 5 ? '#FF6B6B' : seconds <= 10 ? '#F6C87D' : '#2DC6BB'
  return (
    <div className="relative w-12 h-12 flex-shrink-0">
      <svg className="w-12 h-12 -rotate-90" viewBox="0 0 48 48">
        <circle cx="24" cy="24" r={r} fill="none" stroke="#1E2440" strokeWidth="3.5" />
        <circle cx="24" cy="24" r={r} fill="none" stroke={color} strokeWidth="3.5"
          strokeDasharray={`${c * (seconds / TIMER)} ${c}`} strokeLinecap="round"
          style={{ transition: 'stroke-dasharray 1s linear, stroke 0.3s' }} />
      </svg>
      <span className="absolute inset-0 flex items-center justify-center text-xs font-bold font-mono" style={{ color }}>{seconds}</span>
    </div>
  )
}

function TestReview({ resultId, onBack }) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    testsAPI.getReview(resultId).then(setData).catch(() => {}).finally(() => setLoading(false))
  }, [resultId])

  if (loading) return (
    <div className="min-h-screen-safe bg-bg page-enter">
      <TopBar showBack onBack={onBack} title="Жауаптарды қарау" />
      <div className="px-3 pt-2 space-y-2.5">{[0,1,2,3].map(i => <SkeletonCard key={i} />)}</div>
    </div>
  )

  if (!data) return (
    <div className="min-h-screen-safe bg-bg flex items-center justify-center">
      <p className="text-text-3 text-xs">Деректер жүктелмеді</p>
    </div>
  )

  return (
    <div className="min-h-screen-safe bg-bg page-enter">
      <TopBar showBack onBack={onBack} title={`Нәтиже: ${Math.round(data.percentage)}%`} />
      <div className="px-3 pt-1.5 pb-4 space-y-2.5">
        {data.questions.map((q, i) => (
          <div key={i} className={`card p-3 border ${q.correct ? 'border-success/20' : 'border-danger/20'}`}>
            <div className="flex items-center gap-1.5 mb-1.5">
              <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${q.correct ? 'bg-success/10 text-success' : 'bg-danger/10 text-danger'}`}>
                {i + 1}. {q.correct ? 'Дұрыс' : 'Қате'}
              </span>
              <span className="text-[9px] text-text-3">{q.topic}</span>
            </div>
            <p className="text-xs text-text-1 mb-1.5"><FormulaRenderer text={q.question} /></p>
            <QuestionMedia imageUrl={q.image_url} tableData={q.table_data} />
            <div className="space-y-1">
              {q.options.map((opt, oi) => {
                let cls = 'bg-surface border-border text-text-2'
                if (oi === q.correct_answer) cls = 'bg-success/10 border-success text-success'
                else if (oi === q.your_answer && !q.correct) cls = 'bg-danger/10 border-danger text-danger'
                return (
                  <div key={oi} className={`rounded-lg px-2.5 py-1.5 border text-[11px] flex items-center gap-2 ${cls}`}>
                    <span className="font-bold w-4">{String.fromCharCode(65 + oi)}</span>
                    <FormulaRenderer text={opt} />
                  </div>
                )
              })}
            </div>
            {!q.correct && q.explanation && (
              <div className="mt-2 bg-surface-2 rounded-lg px-2.5 py-1.5 border border-border">
                <p className="text-[10px] text-primary font-semibold mb-0.5">Түсіндірме:</p>
                <p className="text-[11px] text-text-2"><FormulaRenderer text={q.explanation} /></p>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

function ResultScreen({ score, total, pct, xpEarned, bonusXp, isDaily, onRetry, onHome, resultId, onReview, newAchievements = [] }) {
  const passed = pct >= 70
  const [showXP, setShowXP] = useState(xpEarned > 0)

  useEffect(() => {
    if (passed) confetti({ particleCount: 140, spread: 85, origin: { y: 0.5 }, colors: ['#2DC6BB', '#3FE0A4', '#E8955A', '#F6C87D', '#F5EEDF'] })
  }, [passed])

  const r = 50, circ = 2 * Math.PI * r
  const mainColor = passed ? '#3FE0A4' : '#E8955A'
  return (
    <div className="h-screen-safe flex flex-col items-center justify-center px-5 page-enter relative overflow-hidden">
      {showXP && (
        <XPAnimation xp={xpEarned} bonusXp={bonusXp} onDone={() => setShowXP(false)} />
      )}
      <Trophy size={54} strokeWidth={1} className="mb-3" style={{ color: passed ? '#F6C87D' : '#5A6078' }} />
      <h2 className="font-display text-[30px] font-bold text-text-1 mb-0.5 leading-none" style={{ fontVariationSettings: "'opsz' 144, 'SOFT' 100" }}>
        {passed ? 'Керемет!' : 'Тырысыңыз!'}
      </h2>
      <p className="text-sm text-text-2 font-medium mb-2">{score} / {total} дұрыс жауап</p>
      {xpEarned > 0 && (
        <div className="flex items-center gap-2 mb-4">
          <div className="flex items-center gap-1 rounded-full px-2.5 py-1 font-mono border"
            style={{ background: 'rgba(45,198,187,0.10)', borderColor: 'rgba(45,198,187,0.30)' }}>
            <Zap size={11} strokeWidth={2} className="text-primary" />
            <span className="text-[11px] font-bold text-primary">+{xpEarned} XP</span>
          </div>
          {bonusXp > 0 && (
            <div className="flex items-center gap-1 rounded-full px-2.5 py-1 font-mono border"
              style={{ background: 'rgba(246,200,125,0.10)', borderColor: 'rgba(246,200,125,0.30)' }}>
              <span className="text-[11px] font-bold text-saffron">+{bonusXp} бонус</span>
            </div>
          )}
        </div>
      )}
      <div className="relative w-32 h-32 mx-auto mb-6">
        <svg className="w-32 h-32 -rotate-90" viewBox="0 0 120 120">
          <circle cx="60" cy="60" r={r} fill="none" stroke="#1E2440" strokeWidth="7" />
          <circle cx="60" cy="60" r={r} fill="none" stroke={mainColor} strokeWidth="7"
            strokeDasharray={`${circ * (pct / 100)} ${circ}`} strokeLinecap="round"
            style={{ transition: 'stroke-dasharray 1.5s cubic-bezier(0.34,1.56,0.64,1)', filter: `drop-shadow(0 0 8px ${mainColor}60)` }} />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="font-display text-[32px] font-bold leading-none" style={{ color: mainColor, fontVariationSettings: "'opsz' 144, 'SOFT' 100" }}>{pct}%</span>
        </div>
      </div>
      {newAchievements.length > 0 && (
        <div className="w-full max-w-xs mb-3 animate-slide-up">
          <p className="text-[10px] text-warning font-semibold uppercase tracking-wider text-center mb-1.5">Жаңа жетістіктер!</p>
          <div className="flex justify-center gap-2">
            {newAchievements.map(a => (
              <div key={a.code} className="card px-3 py-2 text-center border animate-scale-in" style={{ borderColor: `${a.color}40` }}>
                <span className="text-2xl">{a.icon}</span>
                <p className="text-[10px] font-bold text-text-1 mt-0.5">{a.name_kz}</p>
              </div>
            ))}
          </div>
        </div>
      )}
      <div className="flex flex-col gap-2 w-full max-w-xs">
        {resultId && (
          <Button variant="secondary" onClick={() => onReview(resultId)} icon={<BookOpen size={14} />}>Жауаптарды қарау</Button>
        )}
        <div className="flex gap-2.5">
          {!isDaily && <Button variant="secondary" onClick={onRetry} icon={<RotateCcw size={14} />}>Қайтару</Button>}
          <Button onClick={onHome} icon={<Home size={14} />}>Басты бет</Button>
        </div>
      </div>
    </div>
  )
}

function TopicSelect({ topics, loading, onSelect }) {
  if (loading) return (
    <div className="min-h-screen-safe bg-bg page-enter">
      <TopBar />
      <div className="px-3 pt-3 space-y-2.5">
        {[0,1,2,3].map(i => <div key={i} className="skeleton h-16 rounded-xl" />)}
      </div>
    </div>
  )

  return (
    <div className="min-h-screen-safe page-enter">
      <TopBar />
      <div className="px-3 pt-2 pb-4">
        <div className="mb-4">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-[9px] text-terracotta font-semibold uppercase tracking-[0.24em]">Тест</span>
            <span className="h-px flex-1 bg-gradient-to-r from-terracotta/30 to-transparent" />
          </div>
          <h1 className="font-display text-[26px] font-bold text-text-1 leading-tight" style={{ fontVariationSettings: "'opsz' 144, 'SOFT' 100" }}>
            Тақырыпты таңда
          </h1>
          <p className="text-xs text-text-2 font-medium mt-0.5">PISA математика домендері</p>
        </div>

        <button
          onClick={() => onSelect(null)}
          className="relative w-full flex items-center gap-3 rounded-2xl px-4 py-3.5 mb-3 pressable card-lift overflow-hidden"
          style={{
            background: 'linear-gradient(135deg, #2DC6BB 0%, #1FA898 60%, #2DC6BB 100%)',
            boxShadow: '0 16px 32px -16px rgba(45,198,187,0.55), inset 0 1px 0 rgba(255,255,255,0.2)',
          }}
        >
          <span className="absolute inset-0 opacity-30 pointer-events-none"
            style={{ background: 'radial-gradient(ellipse at top right, rgba(246,200,125,0.35) 0%, transparent 60%)' }} />
          <div className="relative w-10 h-10 rounded-xl bg-bg-deep/30 flex items-center justify-center flex-shrink-0 border border-white/20">
            <Shuffle size={19} strokeWidth={2} className="text-bg-deep" />
          </div>
          <div className="relative text-left min-w-0">
            <p className="text-[9px] font-bold text-bg-deep/70 uppercase tracking-[0.2em]">Mix</p>
            <p className="font-display text-[15px] font-bold text-bg-deep leading-tight" style={{ fontVariationSettings: "'opsz' 100, 'SOFT' 50" }}>Аралас тест</p>
            <p className="text-[10px] text-bg-deep/70 font-medium">Барлық тақырыптардан</p>
          </div>
          <ChevronRight size={17} strokeWidth={2.2} className="text-bg-deep/80 ml-auto flex-shrink-0" />
        </button>

        <div className="space-y-2">
          {topics.map((topic, idx) => {
            const accents = ['#2DC6BB', '#E8955A', '#3FE0A4', '#F6C87D']
            const accent = accents[idx % accents.length]
            return (
              <button
                key={topic.id}
                onClick={() => onSelect(topic.id)}
                className="w-full flex items-center gap-3 rounded-2xl px-4 py-3 pressable card-lift"
                style={{
                  background: 'linear-gradient(180deg, #1A2038 0%, #151B2E 100%)',
                  border: '1px solid rgba(232,149,90,0.10)',
                  borderLeft: `3px solid ${accent}`,
                  boxShadow: '0 10px 22px -14px rgba(0,0,0,0.5)',
                }}
              >
                <div className="w-10 h-10 rounded-xl flex items-center justify-center text-lg flex-shrink-0"
                  style={{ background: `${accent}15`, border: `1px solid ${accent}28` }}>
                  {TOPIC_ICONS[topic.id] || (() => { const Icon = TOPIC_LUCIDE_ICONS[topic.id] || BookOpen; return <Icon size={19} strokeWidth={1.6} style={{ color: accent }} /> })()}
                </div>
                <div className="text-left flex-1 min-w-0">
                  <p className="font-display text-[14px] font-bold text-text-1 truncate leading-tight" style={{ fontVariationSettings: "'opsz' 100, 'SOFT' 40" }}>{topic.name}</p>
                  <p className="text-[10px] text-text-3 font-mono mt-0.5">{topic.count} сұрақ</p>
                </div>
                <ChevronRight size={17} strokeWidth={1.6} className="text-text-3 flex-shrink-0" />
              </button>
            )
          })}
        </div>

        {topics.length === 0 && (
          <p className="text-center text-text-3 text-xs mt-6">Тест сұрақтары жоқ</p>
        )}
      </div>
    </div>
  )
}

export default function Test() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const isDaily = searchParams.get('mode') === 'daily'
  const topicParam = searchParams.get('topic')
  const { user, setUser } = useUserStore()

  const [topics, setTopics] = useState([])
  const [topicsLoading, setTopicsLoading] = useState(true)
  const [selectedTopic, setSelectedTopic] = useState(isDaily ? null : topicParam || undefined)

  const [qs, setQs] = useState([])
  const [cur, setCur] = useState(0)
  const [sel, setSel] = useState(null)
  const [answers, setAnswers] = useState([])
  const [loading, setLoading] = useState(false)
  const [done, setDone] = useState(false)
  const [score, setScore] = useState(null)
  const [timer, setTimer] = useState(TIMER)
  const [reviewId, setReviewId] = useState(null)
  const timerRef = useRef(null)

  useEffect(() => {
    testsAPI.getTopics()
      .then(setTopics)
      .catch(() => setTopics([]))
      .finally(() => setTopicsLoading(false))
  }, [])

  const load = useCallback(async (topic) => {
    setLoading(true); setCur(0); setAnswers([]); setSel(null); setDone(false); setScore(null); setTimer(TIMER)
    try {
      const d = isDaily
        ? await testsAPI.getDailyTest()
        : await testsAPI.getTest(topic ? { topic, count: 10 } : { count: 10 })
      setQs(d.questions)
    } catch { setQs([]) }
    finally { setLoading(false) }
  }, [isDaily])

  useEffect(() => {
    if (isDaily) load(null)
    else if (topicParam) load(topicParam)
  }, [isDaily, topicParam])

  const handleTopicSelect = (topicId) => {
    setSelectedTopic(topicId)
    load(topicId)
  }

  const handleRetry = () => { load(selectedTopic) }

  const handleBackToTopics = () => {
    if (isDaily) { navigate('/'); return }
    setSelectedTopic(undefined)
    setDone(false)
    setScore(null)
  }

  useEffect(() => {
    if (loading || done || sel !== null || selectedTopic === undefined) return
    timerRef.current = setInterval(() => {
      setTimer(t => {
        if (t <= 1) { clearInterval(timerRef.current); setSel(-1); WebApp.HapticFeedback.notificationOccurred('warning'); return TIMER }
        return t - 1
      })
    }, 1000)
    return () => clearInterval(timerRef.current)
  }, [cur, loading, done, sel, selectedTopic])

  const handleAnswer = (i) => {
    if (sel !== null) return
    clearInterval(timerRef.current); setSel(i); WebApp.HapticFeedback.impactOccurred('light')
  }

  const handleNext = async () => {
    const newAns = [...answers, { question_id: qs[cur].id, answer: sel ?? -1 }]
    setAnswers(newAns)
    if (cur + 1 < qs.length) { setCur(c => c + 1); setSel(null); setTimer(TIMER) }
    else {
      try {
        const r = await testsAPI.submitTest({ telegram_id: user?.id, answers: newAns, is_daily: isDaily })
        setScore(r); WebApp.HapticFeedback.notificationOccurred(r.percentage >= 70 ? 'success' : 'warning')
        if (user && (r.xp_earned || r.bonus_xp)) {
          setUser({ ...user, score: (user.score || 0) + (r.xp_earned || 0) + (r.bonus_xp || 0) })
        }
      } catch { setScore({ correct: newAns.length, total: qs.length, percentage: 0, xp_earned: 0, bonus_xp: 0 }) }
      setDone(true)
    }
  }

  if (selectedTopic === undefined) {
    return <TopicSelect topics={topics} loading={topicsLoading} onSelect={handleTopicSelect} />
  }

  if (loading) return (
    <div className="min-h-screen-safe bg-bg page-enter">
      <TopBar />
      <div className="px-3 pt-2 space-y-3">
        <SkeletonCard lines={2} />
        {[0,1,2,3].map(i => <div key={i} className="skeleton h-12 rounded-xl" />)}
      </div>
    </div>
  )

  if (reviewId) return (
    <TestReview resultId={reviewId} onBack={() => setReviewId(null)} />
  )

  if (done && score) return (
    <ResultScreen
      score={score.correct}
      total={score.total}
      pct={Math.round(score.percentage)}
      xpEarned={score.xp_earned || 0}
      bonusXp={score.bonus_xp || 0}
      isDaily={isDaily}
      onRetry={handleRetry}
      onHome={handleBackToTopics}
      resultId={score.result_id}
      onReview={(id) => setReviewId(id)}
      newAchievements={score.new_achievements || []}
    />
  )

  const q = qs[cur]
  if (!q) return (
    <div className="h-screen-safe bg-bg flex flex-col items-center justify-center px-5 text-center">
      <p className="text-text-2 text-xs mb-3">Сұрақтар жүктелмеді. Қайтадан көріңіз.</p>
      <Button variant="secondary" onClick={handleBackToTopics}>Артқа</Button>
    </div>
  )

  const topicName = selectedTopic
    ? (topics.find(t => t.id === selectedTopic)?.name ?? selectedTopic)
    : 'Аралас тест'

  return (
    <div className="h-screen-safe bg-bg flex flex-col page-enter">
      <TopBar />
      <div className="flex-1 px-3 pt-2 flex flex-col overflow-hidden">
        <div className="flex items-center gap-2.5 mb-3 flex-shrink-0">
          <div className="flex-1 min-w-0">
            <p className="text-[10px] text-text-2 mb-0.5 truncate">{topicName}</p>
            <p className="text-[10px] text-text-3 mb-1">Сұрақ {cur + 1} / {qs.length}</p>
            <ProgressBar value={cur + 1} max={qs.length} color="primary" size="md" />
          </div>
          <TimerCircle seconds={timer} />
        </div>

        <div className="flex-1 overflow-y-auto no-scrollbar pb-4">
          <div className="card p-3.5 mb-3 animate-slide-up">
            <div className="text-sm break-word">
              <FormulaRenderer text={q.question} />
            </div>
            <QuestionMedia imageUrl={q.image_url} tableData={q.table_data} />
          </div>

          <div className="space-y-2">
            {q.options.map((opt, i) => {
              let cls = 'border-border text-text-1 bg-surface'
              if (sel !== null) {
                if (i === q.correct_answer) cls = 'border-success bg-success/10 text-success'
                else if (i === sel) cls = 'border-danger bg-danger/10 text-danger'
                else cls = 'border-border text-text-3 bg-surface opacity-60'
              }
              return (
                <button key={i} onClick={() => handleAnswer(i)}
                  className={`w-full text-left px-3 py-3 rounded-xl border-2 transition-all duration-200 text-xs font-medium flex items-center gap-2.5 ${cls} ${sel === null ? 'pressable' : ''}`}>
                  <span className={`w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-bold flex-shrink-0 ${
                    sel === null ? 'bg-surface-2 text-text-2' : i === q.correct_answer ? 'bg-success text-bg' : i === sel ? 'bg-danger text-white' : 'bg-surface-2 text-text-3'}`}>
                    {String.fromCharCode(65 + i)}
                  </span>
                  <span className="break-word"><FormulaRenderer text={opt} /></span>
                </button>
              )
            })}
          </div>

          {sel !== null && (
            <div className="mt-3 animate-slide-up">
              {q.explanation && (
                <div className="bg-primary-dim border border-primary/20 rounded-xl p-2.5 mb-2.5 flex gap-2">
                  <Lightbulb size={14} strokeWidth={1.5} className="text-primary flex-shrink-0 mt-0.5" />
                  <p className="text-xs text-text-2 break-word">{q.explanation}</p>
                </div>
              )}
              <Button onClick={handleNext} icon={<ChevronRight size={14} />}>
                {cur + 1 < qs.length ? 'Келесі' : 'Аяқтау'}
              </Button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
