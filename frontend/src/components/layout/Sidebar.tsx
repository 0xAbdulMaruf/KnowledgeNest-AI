import { useState, useEffect } from 'react'
import { Link, useLocation } from 'react-router-dom'
import {
  Home,
  BookOpen,
  Search,
  Sparkles,
  Upload,
  Settings,
  Menu,
  X,
  GraduationCap,
} from 'lucide-react'

const navItems = [
  { path: '/', label: 'Home', icon: Home },
  { path: '/subjects', label: 'Subjects', icon: BookOpen },
  { path: '/search', label: 'Search', icon: Search },
  { path: '/faculty', label: 'Faculty', icon: Upload },
  { path: '/settings', label: 'Settings', icon: Settings },
]

export default function Sidebar() {
  const location = useLocation()
  const [isOpen, setIsOpen] = useState(false)

  useEffect(() => {
    setIsOpen(false)
  }, [location.pathname])

  return (
    <>
      {/* Mobile toggle */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed top-4 left-4 z-50 flex h-10 w-10 items-center justify-center border border-[var(--border)] bg-[var(--bg)] lg:hidden"
      >
        {isOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
      </button>

      {/* Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/60 backdrop-blur-sm lg:hidden"
          onClick={() => setIsOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`fixed top-0 left-0 z-40 flex h-screen w-[240px] flex-col border-r border-[var(--border)] bg-[var(--bg)] transition-transform duration-300 lg:translate-x-0 ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        {/* Logo */}
        <div className="flex h-16 items-center gap-3 border-b border-[var(--border)] px-6">
          <GraduationCap className="h-6 w-6 text-[var(--accent)]" />
          <div>
            <span className="font-[var(--font-display)] text-lg tracking-tight text-[var(--fg)]" style={{ fontFamily: 'var(--font-display)' }}>
              0xCollage
            </span>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 overflow-y-auto p-4">
          <div className="mb-4">
            <p className="mb-3 px-3 font-[var(--font-mono)] text-[0.6875rem] uppercase tracking-[0.14em] text-[var(--muted)]" style={{ fontFamily: 'var(--font-mono)' }}>
              Navigation
            </p>
            <div className="flex flex-col gap-1">
              {navItems.map((item) => {
                const Icon = item.icon
                const isActive = location.pathname === item.path || 
                  (item.path !== '/' && location.pathname.startsWith(item.path))
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={`sidebar-link ${isActive ? 'active' : ''}`}
                  >
                    <Icon className="h-4 w-4" />
                    <span>{item.label}</span>
                  </Link>
                )
              })}
            </div>
          </div>
        </nav>

        {/* Bottom section */}
        <div className="border-t border-[var(--border)] p-4">
          <div className="flex items-center gap-3 px-3">
            <div className="flex h-8 w-8 items-center justify-center border border-[var(--border)]">
              <Sparkles className="h-4 w-4 text-[var(--accent)]" />
            </div>
            <div>
              <p className="text-sm text-[var(--fg)]">AI Assistant</p>
              <p className="font-[var(--font-mono)] text-[0.625rem] uppercase tracking-[0.1em] text-[var(--muted)]" style={{ fontFamily: 'var(--font-mono)' }}>
                Always available
              </p>
            </div>
          </div>
        </div>
      </aside>
    </>
  )
}
