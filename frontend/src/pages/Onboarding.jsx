import { useState, useRef } from 'react'
import WebApp from '@twa-dev/sdk'
import {
  BookOpen, Brain, Bot, Calculator, Trophy,
  CheckCircle2, Flame, Star, Zap, MessageCircle,
  BarChart2, ChevronRight, Sparkles, Sigma,
} from 'lucide-react'
import { useUserStore } from '../store/userStore'
import Button from '../components/Button'

const LEVELS = [
  { id: '1', emoji: '1️⃣', title: 'PISA 1-деңгей', desc: 'Қарапайым есептер',     sub: 'Негізгі амалдар',        color: '#43E97B' },
  { id: '2', emoji: '2️⃣', title: 'PISA 2-деңгей', desc: 'Тәуелділіктерді білемін', sub: 'Формулалар мен сызбалар', color: '#7BE97B' },
  { id: '3', emoji: '3️⃣', title: 'PISA 3-деңгей', desc: 'Бірнеше қадамды есеп',   sub: 'Орташа деңгей',          color: '#FFD93D' },
  { id: '4', emoji: '4️⃣', title: 'PISA 4-деңгей', desc: 'Модельдеу мен талдау',    sub: 'Күрделі контекст',       color: '#FFA63D' },
  { id: '5', emoji: '5️⃣', title: 'PISA 5-деңгей', desc: 'Күрделі модельдер',       sub: 'Стратегиялық ойлау',      color: '#FF6584' },
  { id: '6', emoji: '6️⃣', title: 'PISA 6-деңгей', desc: 'Жоғары деңгей талдау',    sub: 'Математикалық дәлелдеу',  color: '#D93DFF' },
]

const FEATURES = [
  { Icon: BookOpen,       title: 'Теория',           tag: 'Оқу',          desc: '4 PISA домені — формулалар мен түсіндірмелер қазақша.',       color: '#6C63FF', bg: 'rgba(108,99,255,0.12)' },
  { Icon: Calculator,     title: 'Есептер',          tag: 'Тәжірибе',     desc: 'PISA 1-ден 6-ға дейін. Шешімді қадам-қадам тексер.',          color: '#FF6584', bg: 'rgba(255,101,132,0.12)' },
  { Icon: Brain,          title: 'Тест',             tag: 'Тексеру',      desc: '10 сұрақтан тұратын тест. Таймер бар.',                        color: '#43E97B', bg: 'rgba(67,233,123,0.12)' },
  { Icon: Flame,          title: 'Күнделікті сынақ', tag: 'Бонус',        desc: 'Күн сайын жаңа тест — +50 бонус XP!',                         color: '#FFD93D', bg: 'rgba(255,211,61,0.12)' },
  { Icon: MessageCircle,  title: 'AI Репетитор',     tag: 'AI',           desc: 'Математика сұрағын жаз — AI қазақша жауап береді.',            color: '#38BDF8', bg: 'rgba(56,189,248,0.12)' },
  { Icon: Trophy,         title: 'Рейтинг',          tag: 'Жарыс',        desc: 'XP жинап алдыңғы қатарға шық!',                               color: '#FB923C', bg: 'rgba(251,146,60,0.12)' },
  { Icon: BarChart2,      title: 'Прогресс',         tag: 'Статистика',   desc: 'Тақырыптар бойынша үлгерім, streak және нәтижелер.',           color: '#A78BFA', bg: 'rgba(167,139,250,0.12)' },
]

function Dots({ total, current, onClick }) {
  return (
    <div className="flex justify-center items-center gap-1.5 py-3">
      {Array.from({ length: total }).map((_, i) => (
        <button key={i} onClick={() => i <= current && onClick(i)}
          className={`rounded-full transition-all duration-300 ${
            i === current ? 'w-6 h-2 bg-primary shadow-glow-primary' : i < current ? 'w-2 h-2 bg-primary/50' : 'w-2 h-2 bg-border'
          }`} />
      ))}
    </div>
  )
}

/* ─── Screen 0: Welcome ─── */
function Screen0({ onNext, onSkip }) {
  return (
    <div className="flex flex-col h-full px-4">
      <div className="flex justify-end pt-3">
        <button onClick={onSkip} className="text-[10px] text-text-3 bg-surface border border-border rounded-full px-2.5 py-1 pressable">
          Өткізу
        </button>
      </div>

      <div className="flex-1 flex flex-col items-center justify-center">
        <div className="relative w-32 h-32 mx-auto mb-5 flex items-center justify-center">
          <div className="absolute inset-0 rounded-full bg-primary/10 blur-2xl" />
          <div className="absolute inset-0 rounded-full border border-primary/20 animate-spin" style={{ animationDuration: '10s' }} />
          <div className="absolute inset-5 rounded-full border border-secondary/20 animate-spin" style={{ animationDuration: '6s', animationDirection: 'reverse' }} />
          <div className="absolute inset-10 rounded-full border border-success/20 animate-spin" style={{ animationDuration: '4s' }} />
          {[0, 1, 2].map(i => (
            <div key={i} className="absolute inset-0 flex items-start justify-center"
              style={{ transform: `rotate(${i * 120}deg)` }}>
              <div className="w-2.5 h-2.5 rounded-full mt-0.5 shadow-glow-primary"
                style={{ background: ['#6C63FF','#FF6584','#43E97B'][i], boxShadow: `0 0 8px ${['#6C63FF','#FF6584','#43E97B'][i]}` }} />
            </div>
          ))}
          <Sigma size={44} strokeWidth={1.2} className="z-10 text-primary drop-shadow-[0_0_12px_rgba(108,99,255,0.7)]" />
        </div>

        <div className="flex items-center gap-1.5 mb-2">
          <Sparkles size={14} strokeWidth={1.5} className="text-primary" />
          <span className="text-[10px] font-semibold text-primary uppercase tracking-widest">Math PISA Bot</span>
        </div>
        <h1 className="text-2xl font-extrabold text-text-1 text-center mb-2 leading-tight">
          Математиканы<br />оңай үйрен!
        </h1>
        <p className="text-xs text-text-2 text-center leading-relaxed mb-6 max-w-[280px]">
          PISA деңгейіндегі теория, есептер, тесттер және AI репетитор — барлығы қазақ тілінде
        </p>

        <div className="flex flex-wrap justify-center gap-1.5 mb-6">
          {[
            { icon: '📐', text: '4 PISA домен' },
            { icon: '🧠', text: 'AI репетитор' },
            { icon: '🏆', text: 'Рейтинг' },
            { icon: '🔥', text: 'Streak' },
            { icon: '⚡', text: 'XP жүйесі' },
          ].map(({ icon, text }) => (
            <div key={text} className="flex items-center gap-1 bg-surface border border-border rounded-full px-2.5 py-1">
              <span className="text-xs">{icon}</span>
              <span className="text-[10px] text-text-2 font-medium">{text}</span>
            </div>
          ))}
        </div>

        <button onClick={onNext}
          className="w-full max-w-[260px] flex items-center justify-center gap-1.5 bg-gradient-primary rounded-xl py-3.5 font-bold text-white text-sm shadow-glow-primary pressable">
          Бастайық
          <ChevronRight size={16} strokeWidth={2.5} />
        </button>
      </div>
    </div>
  )
}

/* ─── Screen 1: Features ─── */
function Screen1({ onNext, onSkip }) {
  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-between pt-3 px-4 mb-2 flex-shrink-0">
        <h1 className="text-lg font-extrabold text-text-1">Не істей аласың?</h1>
        <button onClick={onSkip} className="text-[10px] text-text-3 pressable underline underline-offset-2">
          өткізу
        </button>
      </div>

      <div className="flex-1 overflow-y-auto no-scrollbar px-4 space-y-2 pb-2">
        {FEATURES.map((feat, i) => (
          <div
            key={i}
            className="flex items-start gap-2.5 rounded-xl p-3 border animate-slide-up"
            style={{
              background: feat.bg,
              borderColor: feat.color + '35',
              animationDelay: `${i * 0.07}s`,
              animationFillMode: 'both',
            }}
          >
            <div
              className="w-9 h-9 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5"
              style={{ background: feat.color + '22', border: `1.5px solid ${feat.color}45` }}
            >
              <feat.Icon size={18} strokeWidth={1.5} style={{ color: feat.color }} />
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-1.5 mb-0.5">
                <span className="text-xs font-bold text-text-1">{feat.title}</span>
                <span
                  className="text-[8px] font-bold rounded-full px-1.5 py-0.5 flex-shrink-0"
                  style={{ background: feat.color + '22', color: feat.color }}
                >
                  {feat.tag}
                </span>
              </div>
              <p className="text-[11px] text-text-2 leading-relaxed">{feat.desc}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="px-4 pt-2 pb-1.5 flex-shrink-0 flex items-center justify-between">
        <p className="text-[10px] text-text-3">Барлық мүмкіндіктер</p>
        <button
          onClick={onNext}
          className="flex items-center gap-1 rounded-lg px-3 py-1.5 text-[11px] font-bold text-white pressable"
          style={{ background: 'rgba(108,99,255,0.85)' }}
        >
          Келесі <ChevronRight size={12} strokeWidth={2.5} />
        </button>
      </div>
    </div>
  )
}

/* ─── Screen 2: Level ─── */
function Screen2({ selectedLevel, onSelect, onStart }) {
  return (
    <div className="flex flex-col h-full px-4">
      <div className="pt-4 pb-3 flex-shrink-0">
        <div className="flex items-center gap-1.5 mb-1.5">
          <Star size={14} strokeWidth={1.5} className="text-warning" />
          <span className="text-[10px] font-semibold text-warning uppercase tracking-widest">Соңғы қадам</span>
        </div>
        <h1 className="text-xl font-extrabold text-text-1 mb-0.5">PISA деңгейіңді таңда</h1>
        <p className="text-xs text-text-2">Есептер қиындығы осыған байланысты</p>
      </div>

      <div className="flex-1 overflow-y-auto no-scrollbar space-y-2 pb-2">
        {LEVELS.map((lvl) => {
          const sel = selectedLevel === lvl.id
          return (
            <button key={lvl.id} onClick={() => {
              onSelect(lvl.id)
              WebApp.HapticFeedback.impactOccurred('medium')
            }}
              className="w-full text-left rounded-xl p-3 border-2 transition-all duration-200 pressable"
              style={{
                borderColor: sel ? lvl.color : 'rgba(255,255,255,0.08)',
                background: sel ? lvl.color + '12' : 'rgba(255,255,255,0.03)',
              }}>
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl flex items-center justify-center text-xl flex-shrink-0"
                  style={{ background: lvl.color + '18', border: `1.5px solid ${lvl.color}40` }}>
                  {lvl.emoji}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="font-bold text-text-1 text-xs mb-0.5">{lvl.title}</div>
                  <div className="text-[11px] text-text-2 truncate">{lvl.desc}</div>
                  <div className="text-[10px] mt-0.5 truncate" style={{ color: lvl.color + 'bb' }}>{lvl.sub}</div>
                </div>
                <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center flex-shrink-0 transition-all duration-200`}
                  style={{ borderColor: sel ? lvl.color : '#333', background: sel ? lvl.color : 'transparent' }}>
                  {sel && <CheckCircle2 size={12} strokeWidth={2.5} className="text-white" />}
                </div>
              </div>
            </button>
          )
        })}

        <p className="text-[10px] text-text-3 text-center pt-1">Деңгейді кейін өзгертуге болады</p>
      </div>

      <button onClick={onStart} disabled={!selectedLevel}
        className={`w-full flex items-center justify-center gap-1.5 rounded-xl py-3.5 font-bold text-sm text-white mt-3 mb-2 flex-shrink-0 transition-all duration-200 ${
          selectedLevel ? 'bg-gradient-primary shadow-glow-primary pressable' : 'bg-surface text-text-3 cursor-not-allowed'
        }`}>
        Қолданбаны ашу
      </button>
    </div>
  )
}

/* ─── Root ─── */
export default function Onboarding({ onComplete }) {
  const [screen, setScreen] = useState(0)
  const [selectedLevel, setSelectedLevel] = useState(null)
  const { user } = useUserStore()
  const touchStartX = useRef(null)

  const handleTouchStart = (e) => { touchStartX.current = e.touches[0].clientX }
  const handleTouchEnd = (e) => {
    if (touchStartX.current === null) return
    const delta = touchStartX.current - e.changedTouches[0].clientX
    if (delta > 50 && screen < 2) setScreen(s => s + 1)
    if (delta < -50 && screen > 0) setScreen(s => s - 1)
    touchStartX.current = null
  }

  const handleStart = async () => {
    if (!selectedLevel) return
    if (user?.id) {
      try {
        const apiUrl = import.meta.env.VITE_API_URL || '/api'
        await fetch(`${apiUrl}/users/level`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ telegram_id: user.id, level: selectedLevel }),
        })
      } catch {}
    }
    WebApp.HapticFeedback.notificationOccurred('success')
    localStorage.setItem('onboarding_completed', 'true')
    onComplete()
  }

  const SKIP = () => setScreen(2)

  const screens = [
    <Screen0 onNext={() => setScreen(1)} onSkip={SKIP} />,
    <Screen1 onNext={() => setScreen(2)} onSkip={SKIP} />,
    <Screen2 selectedLevel={selectedLevel} onSelect={setSelectedLevel} onStart={handleStart} />,
  ]

  return (
    <div className="bg-bg flex flex-col overflow-hidden h-screen-safe"
      onTouchStart={handleTouchStart} onTouchEnd={handleTouchEnd}>

      {/* Progress bar at top */}
      <div className="h-0.5 bg-border flex-shrink-0">
        <div className="h-full bg-primary transition-all duration-500 ease-out"
          style={{ width: `${((screen + 1) / 3) * 100}%` }} />
      </div>

      <div className="flex-1 overflow-hidden">
        {screens[screen]}
      </div>

      <Dots total={3} current={screen} onClick={setScreen} />
    </div>
  )
}
