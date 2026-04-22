import { useNavigate, useLocation } from 'react-router-dom'
import WebApp from '@twa-dev/sdk'
import { Home, BookOpen, Calculator, Brain, MessageCircle, Settings } from 'lucide-react'
import { useUserStore } from '../store/userStore'
import { ADMIN_IDS } from '../pages/Admin'

const TABS = [
  { path: '/', Icon: Home, label: 'Басты' },
  { path: '/theory', Icon: BookOpen, label: 'Теория' },
  { path: '/problems', Icon: Calculator, label: 'Есеп' },
  { path: '/test', Icon: Brain, label: 'Тест' },
  { path: '/ask-ai', Icon: MessageCircle, label: 'AI' },
]

const ADMIN_TAB = { path: '/admin', Icon: Settings, label: 'Admin' }

export default function BottomNav() {
  const navigate = useNavigate()
  const { pathname } = useLocation()
  const { user } = useUserStore()
  const isAdmin = user && ADMIN_IDS.includes(user.id)
  const tabs = isAdmin ? [...TABS, ADMIN_TAB] : TABS

  const handleTab = (path) => {
    if (path === pathname) return
    WebApp.HapticFeedback.impactOccurred('light')
    navigate(path)
  }

  return (
    <div
      className="fixed bottom-0 left-0 right-0 z-50 blur-bg"
      style={{
        background: 'rgba(11,15,31,0.88)',
        borderTop: '1px solid rgba(232,149,90,0.10)',
        paddingBottom: 'max(4px, env(safe-area-inset-bottom))',
      }}
    >
      {/* warm hairline glow along the top of the bar */}
      <div
        className="absolute top-0 left-1/2 -translate-x-1/2 h-px"
        style={{
          width: '70%',
          background: 'linear-gradient(90deg, transparent 0%, rgba(232,149,90,0.35) 50%, transparent 100%)',
        }}
      />
      <div className="flex items-stretch justify-around px-1 pt-1.5">
        {tabs.map(({ path, Icon, label }) => {
          const active = pathname === path
          return (
            <button key={path} onClick={() => handleTab(path)} className="tab-item flex-1 relative">
              {active && (
                <>
                  <span className="absolute top-0 left-1/2 -translate-x-1/2 w-10 h-[2px] bg-primary rounded-full" />
                  <span className="absolute top-0 left-1/2 -translate-x-1/2 w-14 h-6 bg-primary/25 blur-lg rounded-full effect-glow-pulse" />
                  <span className="absolute -top-0.5 left-1/2 -translate-x-1/2 w-1 h-1 rounded-full bg-saffron shadow-glow-warm" />
                </>
              )}
              <Icon
                size={19}
                strokeWidth={active ? 2.1 : 1.5}
                className={`transition-all duration-200 mt-1.5 ${active ? 'text-primary' : 'text-text-3'}`}
              />
              <span className={`text-[10px] font-semibold mt-0.5 transition-colors duration-200 tracking-wide ${active ? 'text-text-1' : 'text-text-3'}`}>
                {label}
              </span>
            </button>
          )
        })}
      </div>
    </div>
  )
}
