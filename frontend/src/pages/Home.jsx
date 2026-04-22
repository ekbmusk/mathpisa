import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import WebApp from '@twa-dev/sdk'
import { BookOpen, Calculator, Brain, Trophy, BarChart2, HelpCircle, Flame, CheckCircle2, ChevronRight, Zap, Sigma, TrendingUp, Shapes, PieChart, AlertTriangle, Lightbulb, Award } from 'lucide-react'
import TopBar from '../components/TopBar'
import ProgressBar from '../components/ProgressBar'
import { QoshkarMuyiz, RhombusBand } from '../components/KazakhOrnament'
import { progressAPI } from '../api/progress'
import { testsAPI } from '../api/tests'
import { useUserStore } from '../store/userStore'

const MENU = [
  { Icon: BookOpen, title: 'Теория', subtitle: 'PISA математика тақырыптары', path: '/theory', accent: '#2DC6BB' },
  { Icon: Calculator, title: 'Есептер', subtitle: 'PISA деңгейлері бойынша', path: '/problems', accent: '#E8955A' },
  { Icon: Brain, title: 'Тест', subtitle: '10 сұрақпен тексер', path: '/test', accent: '#3FE0A4' },
  { Icon: Award, title: 'Жетістіктер', subtitle: 'Медальдар мен бейджіктер', path: '/achievements', accent: '#F6C87D' },
  { Icon: Trophy, title: 'Рейтинг', subtitle: 'Үздік оқушылар', path: '/rating', accent: '#E8955A' },
  { Icon: BarChart2, title: 'Прогресс', subtitle: 'Үлгерім бақылау', path: '/progress', accent: '#7AA7FF' },
  { Icon: HelpCircle, title: 'Көмек', subtitle: 'Нұсқаулық', path: '/help', accent: '#9BA4B8' },
]

const MOTIVATIONS = [
  'Бүгін жаңа нәрсе үйрен!',
  'Математика — ойлау тілі',
  'Формулалар — ойдың коды',
  'Жетістікке жол — тәжірибеден',
  'PISA — сауаттылықтың кілті',
]

export default function Home() {
  const navigate = useNavigate()
  const { user } = useUserStore()
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [dailyStatus, setDailyStatus] = useState(null)
  const [recommendations, setRecommendations] = useState([])
  const motivation = MOTIVATIONS[new Date().getDay() % MOTIVATIONS.length]

  useEffect(() => {
    if (user?.id) {
      progressAPI.getUserProgress(user.id).then(setStats).catch(() => { }).finally(() => setLoading(false))
      testsAPI.getDailyStatus(user.id).then(setDailyStatus).catch(() => {})
      progressAPI.getAnalytics(user.id).then(d => setRecommendations(d?.recommendations || [])).catch(() => {})
    } else setLoading(false)
  }, [user?.id])

  const nav = (path) => { WebApp.HapticFeedback.impactOccurred('light'); navigate(path) }
  const lastTopic = stats?.topics?.find(t => t.percent > 0 && t.percent < 100)

  return (
    <div className="min-h-screen-safe page-enter">
      <TopBar />
      <div className="px-3 space-y-3 pt-2 pb-3">

        {/* Hero — night steppe with warm ornaments */}
        <div className="relative rounded-[26px] overflow-hidden border border-terracotta/15 px-5 py-5 card-lift"
          style={{
            background: 'radial-gradient(ellipse at top right, rgba(232,149,90,0.22) 0%, transparent 55%), radial-gradient(ellipse at bottom left, rgba(45,198,187,0.18) 0%, transparent 55%), linear-gradient(150deg, #1A1E3A 0%, #0F1428 60%, #0B0F1F 100%)',
            boxShadow: '0 20px 40px -20px rgba(0,0,0,0.6), inset 0 1px 0 rgba(246,200,125,0.08)',
          }}>
          {/* slow-spinning ornament behind the content */}
          <div className="absolute -top-6 -right-6 pointer-events-none">
            <div className="animate-ornament-spin opacity-60">
              <QoshkarMuyiz size={140} color="#E8955A" strokeWidth={1.2} opacity={0.35} />
            </div>
          </div>
          <div className="absolute -bottom-10 -left-10 pointer-events-none">
            <QoshkarMuyiz size={110} color="#2DC6BB" strokeWidth={1.1} opacity={0.22} className="rotate-180" />
          </div>

          {/* soft glow orbs */}
          <div className="absolute top-4 right-10 w-20 h-20 rounded-full bg-primary/15 blur-2xl effect-glow-pulse pointer-events-none" />
          <div className="absolute -bottom-6 left-8 w-24 h-24 rounded-full bg-terracotta/12 blur-3xl effect-drift pointer-events-none" />

          {/* tiny math glyphs */}
          <div className="absolute inset-0 overflow-hidden pointer-events-none select-none">
            <span className="particle particle-1 absolute top-3 right-20 text-primary/35 text-base font-mono">∑</span>
            <span className="particle particle-2 absolute top-10 right-8 text-saffron/30 text-[11px] font-mono">π</span>
            <span className="particle particle-3 absolute bottom-5 right-14 text-terracotta/30 text-lg font-mono">∞</span>
          </div>

          <div className="relative z-10">
            <div className="flex items-center gap-2 mb-1">
              <span className="text-[9px] text-saffron/80 font-semibold uppercase tracking-[0.24em]">PISA · Math</span>
              <span className="h-px flex-1 bg-gradient-to-r from-saffron/30 to-transparent" />
            </div>
            <h1 className="font-display text-[28px] leading-[1.05] font-bold text-text-1 mb-1.5" style={{ fontVariationSettings: "'opsz' 144, 'SOFT' 100" }}>
              Сәлем,<br />
              <span className="text-saffron italic" style={{ fontVariationSettings: "'opsz' 144, 'SOFT' 100" }}>{user?.first_name || 'Оқушы'}</span>
            </h1>
            <p className="text-[13px] text-text-2 mb-2.5 font-medium leading-snug max-w-[85%]">{motivation}</p>
            <div className="flex items-center gap-2 flex-wrap">
              {(stats?.streak || 0) > 0 && (
                <div className="inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 border"
                  style={{ background: 'rgba(246,200,125,0.10)', borderColor: 'rgba(246,200,125,0.28)' }}>
                  <Flame size={12} strokeWidth={2.2} className="text-saffron" />
                  <span className="text-saffron text-[11px] font-bold font-mono">{stats.streak}</span>
                  <span className="text-saffron/70 text-[10px]">күн қатар</span>
                </div>
              )}
              <RhombusBand width={72} height={8} color="#E8955A" opacity={0.5} />
            </div>
          </div>
        </div>

        {/* Quick stats */}
        {loading ? (
          <div className="grid grid-cols-4 gap-2">
            {[0, 1, 2, 3].map(i => <div key={i} className="skeleton h-20 rounded-2xl" />)}
          </div>
        ) : (
          <div className="grid grid-cols-4 gap-2">
            {[
              { Icon: Zap, label: 'XP', value: stats?.total_score || 0, tint: 'primary' },
              { Icon: Flame, label: 'Жолақ', value: stats?.streak || 0, tint: 'saffron' },
              { Icon: CheckCircle2, label: 'Есеп', value: stats?.problems_solved || 0, tint: 'success' },
              { Icon: Brain, label: 'Тест', value: stats?.tests_taken || 0, tint: 'terracotta' },
            ].map((s, i) => {
              const colorMap = {
                primary: { bar: '#2DC6BB', text: 'text-primary' },
                saffron: { bar: '#F6C87D', text: 'text-saffron' },
                success: { bar: '#3FE0A4', text: 'text-success' },
                terracotta: { bar: '#E8955A', text: 'text-terracotta' },
              }[s.tint]
              return (
                <div key={i} className="relative rounded-2xl p-2.5 text-center overflow-hidden"
                  style={{
                    background: 'linear-gradient(180deg, #1A2038 0%, #151B2E 100%)',
                    border: '1px solid rgba(232,149,90,0.10)',
                    boxShadow: '0 10px 20px -12px rgba(0,0,0,0.5), inset 0 1px 0 rgba(246,200,125,0.05)',
                  }}>
                  <span className="absolute top-0 left-3 right-3 h-[2px] rounded-full" style={{ background: colorMap.bar, opacity: 0.7 }} />
                  <s.Icon size={17} strokeWidth={1.7} className={`mx-auto mb-1 ${colorMap.text}`} />
                  <div className="font-mono font-bold text-[17px] text-text-1 leading-none">{s.value}</div>
                  <div className="text-[9px] text-text-3 mt-1 uppercase tracking-wider">{s.label}</div>
                </div>
              )
            })}
          </div>
        )}

        {/* Daily challenge */}
        {dailyStatus && (
          <button
            onClick={() => !dailyStatus.completed && nav('/test?mode=daily')}
            className={`w-full rounded-xl p-3 text-left border transition-all ${
              dailyStatus.completed
                ? 'bg-surface border-success/30 opacity-70 cursor-default'
                : 'bg-surface border-warning/30 pressable card-lift shadow-card'
            }`}
          >
            <div className="flex items-center gap-2.5">
              <div className={`w-9 h-9 rounded-lg flex items-center justify-center flex-shrink-0 ${dailyStatus.completed ? 'bg-success/10' : 'bg-warning/10'}`}>
                {dailyStatus.completed
                  ? <CheckCircle2 size={18} strokeWidth={1.5} className="text-success" />
                  : <Flame size={18} strokeWidth={1.5} className="text-warning" />
                }
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-[10px] font-semibold uppercase tracking-wider mb-0.5 text-warning">Күнделікті сынақ</p>
                <p className="text-xs font-bold text-text-1 truncate">
                  {dailyStatus.completed ? 'Бүгін орындалды!' : '10 сұрақ · Бонус XP'}
                </p>
              </div>
              {!dailyStatus.completed && (
                <div className="flex items-center gap-1 bg-warning/10 rounded-full px-2 py-0.5 flex-shrink-0">
                  <Zap size={10} strokeWidth={2} className="text-warning" />
                  <span className="text-[10px] font-bold text-warning">+{dailyStatus.bonus_xp}</span>
                </div>
              )}
            </div>
          </button>
        )}

        {/* Recommendations */}
        {recommendations.length > 0 && (
          <div>
            <div className="flex items-center gap-1 mb-1.5">
              <Lightbulb size={12} strokeWidth={1.5} className="text-warning" />
              <p className="text-[10px] font-semibold text-text-2 uppercase tracking-wider">Ұсыныстар</p>
            </div>
            <div className="space-y-1.5">
              {recommendations.map((rec, i) => (
                <button
                  key={i}
                  onClick={() => nav(rec.action_url)}
                  className="w-full bg-surface border border-warning/20 rounded-xl p-3 text-left pressable shadow-card card-lift"
                >
                  <div className="flex items-center gap-2.5">
                    <div className="w-8 h-8 rounded-lg bg-warning/10 flex items-center justify-center flex-shrink-0">
                      {rec.type === 'review_theory' ? (
                        <AlertTriangle size={16} strokeWidth={1.5} className="text-warning" />
                      ) : (
                        <TrendingUp size={16} strokeWidth={1.5} className="text-primary" />
                      )}
                    </div>
                    <p className="text-xs font-medium text-text-1 flex-1">{rec.message}</p>
                    <ChevronRight size={14} strokeWidth={1.5} className="text-text-3 flex-shrink-0" />
                  </div>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Continue learning */}
        {lastTopic && (
          <button onClick={() => nav('/theory')} className="relative w-full rounded-2xl p-3.5 text-left pressable card-lift overflow-hidden"
            style={{
              background: 'linear-gradient(135deg, rgba(45,198,187,0.14) 0%, #181E36 70%, #151B2E 100%)',
              border: '1px solid rgba(45,198,187,0.28)',
              boxShadow: '0 14px 28px -16px rgba(45,198,187,0.25), inset 0 1px 0 rgba(246,200,125,0.05)',
            }}>
            <div className="absolute -right-4 -bottom-4 opacity-20 pointer-events-none">
              <QoshkarMuyiz size={88} color="#2DC6BB" strokeWidth={1} />
            </div>
            <div className="relative flex items-center justify-between mb-2">
              <div className="min-w-0">
                <p className="text-[9px] text-primary font-semibold uppercase tracking-[0.2em] mb-1">Жалғастыру</p>
                <p className="font-display text-base font-bold text-text-1 truncate leading-tight" style={{ fontVariationSettings: "'opsz' 100, 'SOFT' 50" }}>{lastTopic.name}</p>
              </div>
              <ChevronRight size={18} strokeWidth={1.8} className="text-primary flex-shrink-0" />
            </div>
            <ProgressBar value={lastTopic.percent} max={100} color="primary" showLabel />
          </button>
        )}

        {/* Menu */}
        <div className="pt-1">
          <div className="flex items-center gap-2 mb-2.5 px-0.5">
            <p className="text-[10px] font-bold text-terracotta uppercase tracking-[0.24em]">Бөлімдер</p>
            <span className="h-px flex-1 bg-gradient-to-r from-terracotta/30 via-terracotta/10 to-transparent" />
          </div>
          <div className="space-y-2">
            {MENU.map(({ Icon, title, subtitle, path, accent }) => (
              <button
                key={path}
                onClick={() => nav(path)}
                className="group relative w-full rounded-2xl p-3 text-left pressable card-lift overflow-hidden"
                style={{
                  background: 'linear-gradient(180deg, #1A2038 0%, #151B2E 100%)',
                  border: '1px solid rgba(232,149,90,0.09)',
                  boxShadow: '0 10px 22px -14px rgba(0,0,0,0.5), inset 0 1px 0 rgba(246,200,125,0.04)',
                }}
              >
                {/* left accent bar */}
                <span
                  className="absolute left-0 top-3 bottom-3 w-[3px] rounded-r-full"
                  style={{ background: accent, boxShadow: `0 0 12px ${accent}60` }}
                />
                <div className="flex items-center gap-3 pl-1.5">
                  <div
                    className="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 relative"
                    style={{
                      background: `${accent}15`,
                      border: `1px solid ${accent}28`,
                    }}
                  >
                    <Icon size={19} strokeWidth={1.6} style={{ color: accent }} />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="font-display font-bold text-[14px] text-text-1 leading-tight" style={{ fontVariationSettings: "'opsz' 100, 'SOFT' 40" }}>{title}</div>
                    <div className="text-[10.5px] text-text-2 truncate mt-0.5 font-medium">{subtitle}</div>
                  </div>
                  <ChevronRight size={15} strokeWidth={1.6} className="text-text-3 flex-shrink-0 transition-transform group-active:translate-x-0.5" />
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Ornamental footer strip */}
        <div className="flex justify-center pt-3 pb-1 opacity-70">
          <RhombusBand width={180} height={10} color="#E8955A" opacity={0.45} />
        </div>
      </div>
    </div>
  )
}
