import { useEffect, useState } from 'react'
import { useLocation, useMatch } from 'react-router-dom'
import { Bot, X } from 'lucide-react'
import { useTopic } from '@/hooks/use-api'
import AIAssistantPanel from './AIAssistantPanel'

export default function AIAssistantLauncher() {
  const [isOpen, setIsOpen] = useState(false)
  const topicMatch = useMatch('/topics/:id')
  const location = useLocation()
  const topicId = topicMatch?.params?.id ? Number(topicMatch.params.id) : null
  const { data: topic } = useTopic(topicId || 0)

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setIsOpen(false)
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])

  useEffect(() => {
    setIsOpen(false)
  }, [location.pathname])

  return (
    <>
      <button
        type="button"
        aria-label="Open AI assistant"
        aria-expanded={isOpen}
        onClick={() => setIsOpen((prev) => !prev)}
        className="fixed bottom-5 right-5 z-[80] flex h-14 w-14 items-center justify-center rounded-full border border-[var(--border)] bg-[var(--accent)] text-[var(--bg)] shadow-[0_18px_50px_rgba(0,0,0,0.18)] transition-transform duration-200 hover:scale-105 hover:shadow-[0_20px_60px_rgba(0,0,0,0.22)] focus:outline-none focus:ring-2 focus:ring-[var(--accent)] focus:ring-offset-2 focus:ring-offset-[var(--bg)] md:bottom-8 md:right-8"
      >
        <Bot className="h-6 w-6" />
      </button>

      {isOpen && (
        <div className="fixed inset-0 z-[90]">
          <button
            type="button"
            aria-label="Close AI assistant"
            className="absolute inset-0 bg-black/20 backdrop-blur-[2px]"
            onClick={() => setIsOpen(false)}
          />

          <div className="absolute bottom-0 right-0 left-0 mx-auto flex h-[calc(100vh-4.5rem)] w-full max-w-[calc(100vw-1rem)] items-end justify-end p-2 sm:bottom-5 sm:left-auto sm:right-5 sm:h-[min(86vh,900px)] sm:max-w-[min(980px,calc(100vw-1rem))] sm:p-0">
            <div className="relative flex h-full w-full flex-col overflow-hidden border border-[var(--border)] bg-[var(--bg)] shadow-[0_28px_80px_rgba(0,0,0,0.18)] sm:rounded-2xl">
              <button
                type="button"
                aria-label="Close AI assistant panel"
                onClick={() => setIsOpen(false)}
                className="absolute right-3 top-3 z-10 inline-flex h-9 w-9 items-center justify-center border border-[var(--border)] bg-[var(--bg)] text-[var(--muted)] transition-colors hover:text-[var(--fg)]"
              >
                <X className="h-4 w-4" />
              </button>
              <AIAssistantPanel
                topicId={topicId ?? undefined}
                topicName={topic?.name}
              />
            </div>
          </div>
        </div>
      )}
    </>
  )
}