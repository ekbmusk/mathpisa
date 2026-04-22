/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        bg: '#0B0F1F',
        'bg-deep': '#070A15',
        surface: '#151B2E',
        'surface-2': '#1E2440',
        'surface-3': '#2A3154',

        primary: '#2DC6BB',
        'primary-dim': 'rgba(45,198,187,0.14)',
        'primary-glow': 'rgba(45,198,187,0.35)',

        terracotta: '#E8955A',
        'terracotta-dim': 'rgba(232,149,90,0.14)',
        saffron: '#F6C87D',
        'saffron-dim': 'rgba(246,200,125,0.14)',

        secondary: '#E8955A',

        success: '#3FE0A4',
        warning: '#F6C87D',
        danger: '#FF6B6B',
        info: '#7AA7FF',

        'text-1': '#F5EEDF',
        'text-2': '#9BA4B8',
        'text-3': '#5A6078',

        border: 'rgba(232,149,90,0.09)',
        'border-strong': 'rgba(232,149,90,0.20)',
      },
      fontFamily: {
        sans: ['Manrope', 'system-ui', '-apple-system', 'sans-serif'],
        display: ['Fraunces', 'Georgia', 'serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'monospace'],
      },
      letterSpacing: {
        tightest: '-0.04em',
      },
      animation: {
        'fade-in': 'fadeIn 0.35s ease-out',
        'slide-up': 'slideUp 0.4s cubic-bezier(0.16,1,0.3,1)',
        'slide-down': 'slideDown 0.3s cubic-bezier(0.16,1,0.3,1)',
        'scale-in': 'scaleIn 0.25s ease-out',
        'pulse-slow': 'pulse 3s ease-in-out infinite',
        'float': 'float 6s ease-in-out infinite',
        'shimmer': 'shimmer 1.8s infinite',
        'spin-slow': 'spin 12s linear infinite',
        'ornament-spin': 'ornamentSpin 40s linear infinite',
      },
      keyframes: {
        fadeIn: { from: { opacity: 0 }, to: { opacity: 1 } },
        slideUp: { from: { transform: 'translateY(28px)', opacity: 0 }, to: { transform: 'translateY(0)', opacity: 1 } },
        slideDown: { from: { transform: 'translateY(-20px)', opacity: 0 }, to: { transform: 'translateY(0)', opacity: 1 } },
        scaleIn: { from: { transform: 'scale(0.94)', opacity: 0 }, to: { transform: 'scale(1)', opacity: 1 } },
        float: { '0%,100%': { transform: 'translateY(0)' }, '50%': { transform: 'translateY(-6px)' } },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
        ornamentSpin: { from: { transform: 'rotate(0deg)' }, to: { transform: 'rotate(360deg)' } },
      },
      boxShadow: {
        'glow-primary': '0 0 32px rgba(45,198,187,0.28), 0 0 4px rgba(45,198,187,0.4)',
        'glow-warm': '0 0 36px rgba(232,149,90,0.22)',
        'glow-success': '0 0 26px rgba(63,224,164,0.3)',
        'card': '0 18px 38px -18px rgba(0,0,0,0.55), inset 0 1px 0 rgba(246,200,125,0.04)',
        'sheet': '0 -20px 48px rgba(0,0,0,0.7)',
      },
      backgroundImage: {
        'gradient-primary': 'linear-gradient(135deg, #2DC6BB 0%, #6FE3D9 100%)',
        'gradient-secondary': 'linear-gradient(135deg, #E8955A 0%, #F6C87D 100%)',
        'gradient-warm': 'linear-gradient(135deg, #E8955A 0%, #C24F3A 100%)',
        'gradient-success': 'linear-gradient(135deg, #3FE0A4 0%, #2DC6BB 100%)',
        'gradient-card': 'linear-gradient(180deg, #1C2340 0%, #151B2E 100%)',
        'gradient-hero': 'radial-gradient(ellipse at top left, rgba(45,198,187,0.20) 0%, transparent 55%), radial-gradient(ellipse at bottom right, rgba(232,149,90,0.18) 0%, transparent 60%), linear-gradient(180deg, #0F1428 0%, #0B0F1F 100%)',
        'shimmer-bg': 'linear-gradient(90deg, #151B2E 25%, #1E2440 50%, #151B2E 75%)',
      },
    },
  },
  plugins: [],
}
