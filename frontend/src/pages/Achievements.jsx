import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import WebApp from '@twa-dev/sdk'
import { Lock } from 'lucide-react'
import TopBar from '../components/TopBar'
import { SkeletonCard } from '../components/SkeletonLoader'
import { useUserStore } from '../store/userStore'
import client from '../api/client'

const CATEGORIES = [
  { id: null, label: 'Барлығы' },
  { id: 'xp', label: 'XP' },
  { id: 'streak', label: 'Жолақ' },
  { id: 'test', label: 'Тест' },
  { id: 'special', label: 'Арнайы' },
]

export default function Achievements() {
  const navigate = useNavigate()
  const { user } = useUserStore()
  const [achievements, setAchievements] = useState([])
  const [loading, setLoading] = useState(true)
  const [category, setCategory] = useState(null)

  useEffect(() => {
    WebApp.BackButton.show()
    WebApp.BackButton.onClick(() => navigate('/'))
    if (user?.id) {
      client.get(`/users/${user.id}/achievements`)
        .then(setAchievements)
        .catch(() => {})
        .finally(() => setLoading(false))
    } else setLoading(false)
    return () => WebApp.BackButton.hide()
  }, [user?.id])

  const filtered = category
    ? achievements.filter(a => a.category === category)
    : achievements
  const unlocked = achievements.filter(a => a.unlocked).length

  return (
    <div className="min-h-screen-safe bg-bg page-enter">
      <TopBar showBack onBack={() => navigate('/')} title="Жетістіктер" />
      <div className="px-3 pt-1.5 pb-4">
        <div className="flex items-center justify-between mb-3">
          <div>
            <h1 className="text-xl font-extrabold text-text-1">Жетістіктер</h1>
            <p className="text-xs text-text-2">{unlocked} / {achievements.length} ашылған</p>
          </div>
          <div className="w-12 h-12 rounded-xl bg-warning/10 border border-warning/20 flex items-center justify-center text-2xl">
            🏆
          </div>
        </div>

        <div className="flex gap-1.5 overflow-x-auto no-scrollbar pb-1 mb-3">
          {CATEGORIES.map(c => (
            <button key={String(c.id)} onClick={() => { setCategory(c.id); WebApp.HapticFeedback.impactOccurred('light') }}
              className={`chip flex-shrink-0 border ${category === c.id ? 'bg-primary text-white border-transparent' : 'bg-surface text-text-2 border-border'}`}>
              {c.label}
            </button>
          ))}
        </div>

        {loading ? (
          <div className="grid grid-cols-2 gap-2">{[0,1,2,3].map(i => <div key={i} className="skeleton h-28 rounded-xl" />)}</div>
        ) : (
          <div className="grid grid-cols-2 gap-2">
            {filtered.map(a => (
              <div key={a.code}
                className={`card p-3 text-center transition-all ${a.unlocked ? 'border-transparent' : 'opacity-50'}`}
                style={a.unlocked ? { borderColor: `${a.color}30`, background: `linear-gradient(135deg, ${a.color}08 0%, #1A1A2E 100%)` } : {}}>
                <div className="text-3xl mb-1.5">
                  {a.unlocked ? a.icon : <Lock size={24} strokeWidth={1} className="mx-auto text-text-3" />}
                </div>
                <p className="text-xs font-bold text-text-1 mb-0.5">{a.name_kz}</p>
                <p className="text-[10px] text-text-3 leading-tight">{a.description_kz}</p>
                {a.unlocked_at && (
                  <p className="text-[9px] text-primary mt-1">{a.unlocked_at}</p>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
