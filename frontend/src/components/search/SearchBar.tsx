import { useState, useRef, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { Search, BookOpen, FileText } from 'lucide-react'
import { useSearch } from '@/hooks/use-api'
import { cn } from '@/lib/utils'

interface SearchBarProps {
  defaultValue?: string
  placeholder?: string
  className?: string
  size?: 'sm' | 'lg'
}

export default function SearchBar({ defaultValue = '', placeholder = 'Search topics, subjects...', className, size = 'sm' }: SearchBarProps) {
  const navigate = useNavigate()
  const [query, setQuery] = useState(defaultValue)
  const [isOpen, setIsOpen] = useState(false)
  const [selectedIndex, setSelectedIndex] = useState(-1)
  const inputRef = useRef<HTMLInputElement>(null)
  const dropdownRef = useRef<HTMLDivElement>(null)

  const { data: searchResults } = useSearch(query.length >= 2 ? query : '')

  const allResults = [
    ...(searchResults?.subjects || []).map((s) => ({ ...s, type: 'subject' as const })),
    ...(searchResults?.topics || []).map((t) => ({ ...t, type: 'topic' as const })),
  ]

  const handleNavigate = useCallback((path: string) => {
    navigate(path)
    setQuery('')
    setIsOpen(false)
    setSelectedIndex(-1)
  }, [navigate])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (query.trim()) {
      handleNavigate(`/search?q=${encodeURIComponent(query.trim())}`)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (!isOpen || allResults.length === 0) {
      if (e.key === 'Enter') handleSubmit(e)
      return
    }

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault()
        setSelectedIndex((prev) => (prev < allResults.length - 1 ? prev + 1 : 0))
        break
      case 'ArrowUp':
        e.preventDefault()
        setSelectedIndex((prev) => (prev > 0 ? prev - 1 : allResults.length - 1))
        break
      case 'Enter':
        e.preventDefault()
        if (selectedIndex >= 0 && selectedIndex < allResults.length) {
          const result = allResults[selectedIndex]
          const path = result.type === 'subject' ? `/subjects/${result.id}` : `/topics/${result.id}`
          handleNavigate(path)
        } else {
          handleSubmit(e)
        }
        break
      case 'Escape':
        setIsOpen(false)
        setSelectedIndex(-1)
        break
    }
  }

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setIsOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  return (
    <div className={cn('relative', className)} ref={dropdownRef} style={{ zIndex: 20 }}>
    <form onSubmit={handleSubmit}>
      <div className="relative">
        <Search className={`absolute left-4 top-1/2 -translate-y-1/2 text-[var(--muted)] ${size === 'lg' ? 'h-5 w-5' : 'h-4 w-4'}`} />
        <input
          ref={inputRef}
          type="text"
          placeholder={placeholder}
          value={query}
          onChange={(e) => {
            setQuery(e.target.value)
            setIsOpen(e.target.value.length >= 2)
            setSelectedIndex(-1)
          }}
          onFocus={() => query.length >= 2 && setIsOpen(true)}
          onKeyDown={handleKeyDown}
          style={{
            width: '100%',
            height: size === 'lg' ? '56px' : '40px',
            fontSize: size === 'lg' ? '18px' : '14px',
            paddingLeft: '48px',
            paddingRight: '16px',
            border: '1px solid var(--border)',
            borderRadius: 'var(--radius)',
            background: 'var(--surface)',
            color: 'var(--fg)',
            outline: 'none',
            transition: 'border-color 0.2s ease, box-shadow 0.2s ease',
          }}
          onFocusCapture={(e) => {
            e.currentTarget.style.borderColor = 'var(--accent)'
            e.currentTarget.style.boxShadow = '0 0 0 2px rgba(201, 100, 66, 0.15)'
          }}
          onBlurCapture={(e) => {
            e.currentTarget.style.borderColor = 'var(--border)'
            e.currentTarget.style.boxShadow = 'none'
          }}
        />
      </div>

      {isOpen && allResults.length > 0 && (
        <div
          style={{
            position: 'absolute',
            top: '100%',
            left: 0,
            right: 0,
            marginTop: '8px',
            maxHeight: '320px',
            overflowY: 'auto',
            border: '1px solid var(--border)',
            borderRadius: 'var(--radius)',
            background: 'var(--surface)',
            boxShadow: '0 12px 40px rgba(0,0,0,0.12)',
            zIndex: 100,
          }}
        >
          {searchResults?.subjects && searchResults.subjects.length > 0 && (
            <div>
              <div className="px-4 py-2 text-[10px] font-semibold uppercase tracking-[0.14em] text-[var(--muted)] font-[var(--font-mono)]" style={{ fontFamily: 'var(--font-mono)' }}>
                Subjects
              </div>
              {searchResults.subjects.map((subject) => {
                const idx = allResults.findIndex((r) => r.id === subject.id && r.type === 'subject')
                return (
                  <button
                    key={`s-${subject.id}`}
                    type="button"
                    onClick={() => handleNavigate(`/subjects/${subject.id}`)}
                    className={cn(
                      'flex w-full items-center gap-3 px-4 py-3 text-left transition-colors border-l-2 border-transparent',
                      selectedIndex === idx 
                        ? 'bg-[var(--bg)] text-[var(--accent)] border-l-[var(--accent)]' 
                        : 'hover:bg-[var(--bg)] hover:text-[var(--fg)]'
                    )}
                  >
                    <BookOpen className="h-4 w-4 text-[var(--accent)] shrink-0" />
                    <div className="min-w-0">
                      <p className="text-sm font-medium text-[var(--fg)] truncate">{subject.name}</p>
                      {subject.code && <p className="text-xs text-[var(--muted)] font-[var(--font-mono)]" style={{ fontFamily: 'var(--font-mono)' }}>{subject.code}</p>}
                    </div>
                  </button>
                )
              })}
            </div>
          )}
          {searchResults?.topics && searchResults.topics.length > 0 && (
            <div>
              <div className="px-4 py-2 text-[10px] font-semibold uppercase tracking-[0.14em] text-[var(--muted)] font-[var(--font-mono)] border-t border-[var(--border)]" style={{ fontFamily: 'var(--font-mono)' }}>
                Topics
              </div>
              {searchResults.topics.slice(0, 6).map((topic) => {
                const idx = allResults.findIndex((r) => r.id === topic.id && r.type === 'topic')
                return (
                  <button
                    key={`t-${topic.id}`}
                    type="button"
                    onClick={() => handleNavigate(`/topics/${topic.id}`)}
                    className={cn(
                      'flex w-full items-center gap-3 px-4 py-3 text-left transition-colors border-l-2 border-transparent',
                      selectedIndex === idx 
                        ? 'bg-[var(--bg)] text-[var(--accent)] border-l-[var(--accent)]' 
                        : 'hover:bg-[var(--bg)] hover:text-[var(--fg)]'
                    )}
                  >
                    <FileText className="h-4 w-4 text-[var(--muted)] shrink-0" />
                    <div className="min-w-0">
                      <p className="text-sm font-medium text-[var(--fg)] truncate">{topic.name}</p>
                      {topic.unit_name && <p className="text-xs text-[var(--muted)]">{topic.unit_name}</p>}
                    </div>
                  </button>
                )
              })}
            </div>
          )}
        </div>
      )}
    </form>
    </div>
  )
}
