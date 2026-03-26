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
      className="fixed bottom-0 left-0 right-0 z-50 blur-bg border-t border-border"
      style={{ background: 'rgba(15,15,26,0.92)', paddingBottom: 'max(4px, env(safe-area-inset-bottom))' }}
    >
      <div className="flex items-stretch justify-around px-1 pt-1.5">
        {tabs.map(({ path, Icon, label }) => {
          const active = pathname === path
          return (
            <button key={path} onClick={() => handleTab(path)} className="tab-item flex-1 relative">
              {active && (
                <span className="absolute top-0 left-1/2 -translate-x-1/2 w-8 h-0.5 bg-primary rounded-full" />
              )}
              {active && (
                <span className="absolute top-0.5 left-1/2 -translate-x-1/2 w-10 h-5 bg-primary/20 blur-md rounded-full effect-glow-pulse" />
              )}
              <Icon
                size={18}
                strokeWidth={active ? 2 : 1.5}
                className={`transition-all duration-200 ${active ? 'text-primary' : 'text-text-3'}`}
              />
              <span className={`text-[10px] font-medium mt-0.5 transition-colors duration-200 ${active ? 'text-primary' : 'text-text-3'}`}>
                {label}
              </span>
            </button>
          )
        })}
      </div>
    </div>
  )
}
