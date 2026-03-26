import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import WebApp from '@twa-dev/sdk'
import { BookOpen, Calculator, Brain, Trophy, BarChart2, HelpCircle, Flame, CheckCircle2, ChevronRight, Zap, Sigma, TrendingUp, Shapes, PieChart, AlertTriangle, Lightbulb, Award } from 'lucide-react'
import TopBar from '../components/TopBar'
import ProgressBar from '../components/ProgressBar'
import { progressAPI } from '../api/progress'
import { testsAPI } from '../api/tests'
import { useUserStore } from '../store/userStore'

const MENU = [
  { Icon: BookOpen, title: 'Теория', subtitle: 'PISA математика тақырыптары', path: '/theory', accent: '#6C63FF' },
  { Icon: Calculator, title: 'Есептер', subtitle: 'PISA деңгейлері бойынша', path: '/problems', accent: '#FF6584' },
  { Icon: Brain, title: 'Тест', subtitle: '10 сұрақпен тексер', path: '/test', accent: '#43E97B' },
  { Icon: Award, title: 'Жетістіктер', subtitle: 'Медальдар мен бейджіктер', path: '/achievements', accent: '#FFD93D' },
  { Icon: Trophy, title: 'Рейтинг', subtitle: 'Үздік оқушылар', path: '/rating', accent: '#FF6584' },
  { Icon: BarChart2, title: 'Прогресс', subtitle: 'Үлгерім бақылау', path: '/progress', accent: '#38BDF8' },
  { Icon: HelpCircle, title: 'Көмек', subtitle: 'Нұсқаулық', path: '/help', accent: '#8B8FA8' },
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
    <div className="min-h-screen-safe bg-bg page-enter">
      <TopBar />
      <div className="px-3 space-y-3 pt-1.5 pb-3">

        {/* Hero */}
        <div className="relative rounded-2xl overflow-hidden border border-primary/20 p-4 shadow-glow-primary/10 card-lift"
          style={{ background: 'linear-gradient(135deg, rgba(108,99,255,0.15) 0%, #1A1A2E 60%, #0F0F1A 100%)' }}>
          <div className="absolute -top-8 -right-8 w-24 h-24 rounded-full bg-primary/20 blur-2xl effect-glow-pulse" />
          <div className="absolute -bottom-10 -left-8 w-20 h-20 rounded-full bg-secondary/20 blur-2xl effect-drift" />
          <div className="absolute inset-0 overflow-hidden pointer-events-none select-none">
            <span className="particle particle-1 absolute top-2 right-6 text-primary/25 text-lg font-mono">∑</span>
            <span className="particle particle-2 absolute top-8 right-14 text-secondary/20 text-xs font-mono">π</span>
            <span className="particle particle-3 absolute bottom-4 right-4 text-primary/20 text-xl font-mono">∞</span>
          </div>
          <div className="relative z-10">
            <p className="text-[10px] text-primary font-semibold uppercase tracking-wider mb-0.5">Математика PISA</p>
            <h1 className="text-xl font-extrabold text-text-1 mb-0.5">
              Сәлем, {user?.first_name || 'Оқушы'}!
            </h1>
            <p className="text-xs text-text-2 mb-2">{motivation}</p>
            {(stats?.streak || 0) > 0 && (
              <div className="inline-flex items-center gap-1 bg-warning/10 border border-warning/25 rounded-full px-2.5 py-0.5">
                <Flame size={12} strokeWidth={2} className="text-warning" />
                <span className="text-warning text-[11px] font-semibold">{stats.streak} күн қатар</span>
              </div>
            )}
          </div>
        </div>

        {/* Quick stats */}
        {loading ? (
          <div className="grid grid-cols-3 gap-2">
            {[0, 1, 2].map(i => <div key={i} className="skeleton h-16 rounded-xl" />)}
          </div>
        ) : (
          <div className="grid grid-cols-4 gap-2">
            {[
              { Icon: Zap, label: 'XP', value: stats?.total_score || 0, color: 'text-primary' },
              { Icon: Flame, label: 'Жолақ', value: stats?.streak || 0, color: 'text-warning' },
              { Icon: CheckCircle2, label: 'Есеп', value: stats?.problems_solved || 0, color: 'text-success' },
              { Icon: Brain, label: 'Тест', value: stats?.tests_taken || 0, color: 'text-info' },
            ].map((s, i) => (
              <div key={i} className="bg-surface border border-border rounded-xl p-2.5 text-center shadow-card">
                <s.Icon size={18} strokeWidth={1.5} className={`mx-auto mb-1 ${s.color}`} />
                <div className="text-base font-bold text-text-1">{s.value}</div>
                <div className="text-[10px] text-text-2">{s.label}</div>
              </div>
            ))}
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
          <button onClick={() => nav('/theory')} className="w-full bg-surface border border-primary/25 rounded-xl p-3 text-left pressable shadow-card card-lift">
            <div className="flex items-center justify-between mb-2">
              <div className="min-w-0">
                <p className="text-[9px] text-primary font-semibold uppercase tracking-wider mb-0.5">Жалғастыру</p>
                <p className="text-xs font-bold text-text-1 truncate">{lastTopic.name}</p>
              </div>
              <ChevronRight size={16} strokeWidth={1.5} className="text-primary/60 flex-shrink-0" />
            </div>
            <ProgressBar value={lastTopic.percent} max={100} color="primary" showLabel />
          </button>
        )}

        {/* Menu */}
        <div>
          <p className="text-[10px] font-semibold text-text-2 uppercase tracking-wider mb-2">Бөлімдер</p>
          <div className="space-y-1.5">
            {MENU.map(({ Icon, title, subtitle, path, accent }) => (
              <button
                key={path}
                onClick={() => nav(path)}
                className="w-full bg-surface border border-border rounded-xl p-3 text-left pressable shadow-card card-lift"
                style={{ borderLeft: `3px solid ${accent}` }}
              >
                <div className="flex items-center gap-2.5">
                  <div className="w-9 h-9 rounded-lg flex items-center justify-center flex-shrink-0" style={{ background: `${accent}18` }}>
                    <Icon size={18} strokeWidth={1.5} style={{ color: accent }} />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="font-semibold text-text-1 text-xs">{title}</div>
                    <div className="text-[10px] text-text-2 truncate mt-0.5">{subtitle}</div>
                  </div>
                  <ChevronRight size={14} strokeWidth={1.5} className="text-text-3 flex-shrink-0" />
                </div>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
