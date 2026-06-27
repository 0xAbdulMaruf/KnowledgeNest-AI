import { useState, useEffect, useRef } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { Search, Menu, X } from 'lucide-react'

export default function Header() {
  const location = useLocation()
  const navigate = useNavigate()
  const [searchQuery, setSearchQuery] = useState('')
  const [isSearchFocused, setIsSearchFocused] = useState(false)
  const [isHeaderHidden, setIsHeaderHidden] = useState(false)
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const searchRef = useRef<HTMLInputElement>(null)

  const navItems = [
    { label: 'Home', path: '/' },
    { label: 'Subjects', path: '/subjects' },
    { label: 'Search', path: '/search' },
    { label: 'Faculty', path: '/faculty' },
  ]

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    if (searchQuery.trim()) {
      navigate(`/search?q=${encodeURIComponent(searchQuery.trim())}`)
      setSearchQuery('')
      searchRef.current?.blur()
      setIsMobileMenuOpen(false)
    }
  }

  // Headroom: hide on scroll down, show on scroll up
  useEffect(() => {
    let lastScroll = 0
    const threshold = 8

    const handleScroll = () => {
      const currentScroll = window.pageYOffset || document.documentElement.scrollTop
      if (currentScroll <= 0) {
        setIsHeaderHidden(false)
        lastScroll = 0
        return
      }
      if (currentScroll - lastScroll > threshold && currentScroll > 80) {
        setIsHeaderHidden(true)
      } else if (lastScroll - currentScroll > threshold) {
        setIsHeaderHidden(false)
      }
      lastScroll = currentScroll
    }

    window.addEventListener('scroll', handleScroll, { passive: true })
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  // Ctrl/Cmd + K shortcut
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault()
        searchRef.current?.focus()
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])

  return (
    <>
      <header
        className={`header-nav ${isHeaderHidden ? 'header-nav--hidden' : ''}`}
        style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          zIndex: 50,
          height: '64px',
          borderBottom: '1px solid var(--border)',
          background: 'var(--bg)',
          backdropFilter: 'blur(12px)',
          padding: '0 24px',
        }}
      >
        <div
          style={{
            maxWidth: '1200px',
            margin: '0 auto',
            height: '100%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: '24px',
          }}
        >
          {/* Logo */}
          <Link to="/" style={{ display: 'flex', alignItems: 'center', gap: '10px', textDecoration: 'none' }}>
            <img src="/logo.png" alt="KnowledgeNest AI" style={{ height: '36px', width: '36px', objectFit: 'contain' }} />
            <span style={{ fontFamily: 'var(--font-display)', fontSize: '18px', fontWeight: 700, color: 'var(--fg)', letterSpacing: '-0.02em' }}>
              KnowledgeNest AI
            </span>
          </Link>

          {/* Desktop Nav */}
          <nav style={{ display: 'flex', alignItems: 'center', gap: '32px' }} className="hidden md:flex">
            {navItems.map((item) => {
              const isActive = location.pathname === item.path
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  style={{
                    fontSize: '14px',
                    fontWeight: isActive ? 600 : 500,
                    color: isActive ? 'var(--accent)' : 'var(--muted)',
                    textDecoration: 'none',
                    transition: 'color 0.2s ease',
                  }}
                  onMouseEnter={(e) => !isActive && (e.currentTarget.style.color = 'var(--fg)')}
                  onMouseLeave={(e) => !isActive && (e.currentTarget.style.color = 'var(--muted)')}
                >
                  {item.label}
                </Link>
              )
            })}
          </nav>

          {/* Desktop Search + CTA */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }} className="hidden md:flex">
            <form onSubmit={handleSearch}>
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  border: `1px solid ${isSearchFocused ? 'var(--accent)' : 'var(--border)'}`,
                  borderRadius: 'var(--radius)',
                  padding: '6px 12px',
                  background: isSearchFocused ? 'var(--surface)' : 'var(--bg)',
                  transition: 'all 0.2s ease',
                }}
              >
                <Search style={{ width: '14px', height: '14px', color: 'var(--muted)' }} />
                <input
                  ref={searchRef}
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onFocus={() => setIsSearchFocused(true)}
                  onBlur={() => setIsSearchFocused(false)}
                  placeholder="Search..."
                  style={{
                    width: isSearchFocused ? '180px' : '120px',
                    border: 'none',
                    outline: 'none',
                    background: 'transparent',
                    fontSize: '13px',
                    color: 'var(--fg)',
                    transition: 'width 0.3s ease',
                  }}
                />
                <kbd
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '2px',
                    border: '1px solid var(--border)',
                    borderRadius: '4px',
                    padding: '1px 6px',
                    fontFamily: 'var(--font-mono)',
                    fontSize: '10px',
                    color: 'var(--muted)',
                  }}
                >
                  ⌘K
                </kbd>
              </div>
            </form>

            <button
              onClick={() => navigate('/subjects')}
              style={{
                padding: '7px 18px',
                fontSize: '13px',
                fontWeight: 600,
                background: 'var(--accent)',
                color: '#fff',
                border: 'none',
                borderRadius: '9999px',
                cursor: 'pointer',
                transition: 'opacity 0.2s ease',
              }}
              onMouseEnter={(e) => (e.currentTarget.style.opacity = '0.85')}
              onMouseLeave={(e) => (e.currentTarget.style.opacity = '1')}
            >
              Get started
            </button>
          </div>

          {/* Mobile toggle */}
          <button
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className="md:hidden"
            style={{ padding: '6px', color: 'var(--muted)', background: 'none', border: 'none', cursor: 'pointer' }}
          >
            {isMobileMenuOpen ? <X style={{ width: '20px', height: '20px' }} /> : <Menu style={{ width: '20px', height: '20px' }} />}
          </button>
        </div>
      </header>

      {/* Mobile Menu */}
      {isMobileMenuOpen && (
        <div
          style={{
            position: 'fixed',
            inset: 0,
            zIndex: 40,
            background: 'var(--bg)',
            paddingTop: '80px',
            paddingLeft: '24px',
            paddingRight: '24px',
          }}
          className="md:hidden"
        >
          <nav style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            {navItems.map((item) => {
              const isActive = location.pathname === item.path
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  onClick={() => setIsMobileMenuOpen(false)}
                  style={{
                    fontSize: '18px',
                    fontWeight: 500,
                    color: isActive ? 'var(--accent)' : 'var(--muted)',
                    borderBottom: '1px solid var(--border)',
                    paddingBottom: '12px',
                    textDecoration: 'none',
                  }}
                >
                  {item.label}
                </Link>
              )
            })}
          </nav>
        </div>
      )}
    </>
  )
}
