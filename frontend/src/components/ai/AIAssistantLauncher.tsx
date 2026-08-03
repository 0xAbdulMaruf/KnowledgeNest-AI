import { useEffect, useRef, useState } from 'react'
import { useLocation, useMatch } from 'react-router-dom'
import { Bot, Maximize2, Minimize2, X } from 'lucide-react'
import { useTopic } from '@/hooks/use-api'
import AIAssistantPanel from './AIAssistantPanel'

export default function AIAssistantLauncher() {
  const [isOpen, setIsOpen] = useState(false)
  const [isClosing, setIsClosing] = useState(false)
  const [isFullscreen, setIsFullscreen] = useState(false)
  const launcherRef = useRef<HTMLButtonElement>(null)
  const closeTimerRef = useRef<number | null>(null)
  const topicMatch = useMatch('/topics/:id')
  const location = useLocation()
  const topicId = topicMatch?.params?.id ? Number(topicMatch.params.id) : null
  const { data: topic } = useTopic(topicId || 0)

  const openAssistant = () => {
    if (closeTimerRef.current !== null) {
      window.clearTimeout(closeTimerRef.current)
      closeTimerRef.current = null
    }
    setIsClosing(false)
    setIsFullscreen(false)
    setIsOpen(true)
  }

  const closeAssistant = () => {
    if (!isOpen || isClosing) return
    setIsClosing(true)
    closeTimerRef.current = window.setTimeout(() => {
      setIsOpen(false)
      setIsClosing(false)
      setIsFullscreen(false)
      closeTimerRef.current = null
      launcherRef.current?.focus()
    }, 280)
  }

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') closeAssistant()
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  })

  useEffect(() => () => {
    if (closeTimerRef.current !== null) window.clearTimeout(closeTimerRef.current)
  }, [])

  useEffect(() => {
    closeAssistant()
  }, [location.pathname])

  return (
    <>
      <button
        type="button"
        aria-label="Open AI assistant"
        aria-expanded={isOpen && !isClosing}
        ref={launcherRef}
        onClick={() => (isOpen ? closeAssistant() : openAssistant())}
        className="fixed bottom-5 right-5 z-[80] flex h-14 w-14 items-center justify-center rounded-full border border-[var(--border)] bg-[var(--accent)] text-[var(--bg)] shadow-[0_18px_50px_rgba(0,0,0,0.18)] transition-transform duration-200 hover:scale-105 hover:shadow-[0_20px_60px_rgba(0,0,0,0.22)] focus:outline-none focus:ring-2 focus:ring-[var(--accent)] focus:ring-offset-2 focus:ring-offset-[var(--bg)] md:bottom-8 md:right-8"
      >
        <Bot className="h-6 w-6" />
      </button>

      {isOpen && (
        <div className={`ai-assistant-layer fixed inset-0 z-[90] ${isClosing ? 'ai-assistant-layer--closing' : ''}`} role="dialog" aria-modal="true" aria-label="AI Assistant">
          <button
            type="button"
            aria-label="Close AI assistant"
            className="ai-assistant-backdrop absolute inset-0 bg-black/20 backdrop-blur-[2px]"
            onClick={closeAssistant}
          />

          <div className={`ai-assistant-window-shell ${isFullscreen ? 'absolute inset-0 h-screen w-screen' : 'absolute bottom-24 right-5 h-[min(620px,calc(100vh-8rem))] w-[min(440px,calc(100vw-2.5rem))] md:right-8'}`}>
            <div className={`ai-assistant-window relative flex h-full w-full flex-col overflow-hidden border border-[var(--border)] bg-[var(--bg)] shadow-[0_28px_80px_rgba(0,0,0,0.24)] ${isFullscreen ? '' : 'rounded-2xl'}`}>
              <div className="absolute right-3 top-3 z-10 flex items-center gap-1">
                <button
                  type="button"
                  aria-label={isFullscreen ? 'Restore AI assistant window' : 'Maximize AI assistant'}
                  title={isFullscreen ? 'Restore window' : 'Full screen'}
                  onClick={() => setIsFullscreen((current) => !current)}
                  className="inline-flex h-9 w-9 items-center justify-center border border-[var(--border)] bg-[var(--bg)] text-[var(--muted)] transition-colors hover:text-[var(--fg)]"
                >
                  {isFullscreen ? <Minimize2 className="h-4 w-4" /> : <Maximize2 className="h-4 w-4" />}
                </button>
                <button
                  type="button"
                  aria-label="Close AI assistant panel"
                  onClick={closeAssistant}
                  className="inline-flex h-9 w-9 items-center justify-center border border-[var(--border)] bg-[var(--bg)] text-[var(--muted)] transition-colors hover:text-[var(--fg)]"
                >
                  <X className="h-4 w-4" />
                </button>
              </div>
              <AIAssistantPanel
                key={topicId ?? 'general'}
                topicId={topicId ?? undefined}
                topicName={topic?.name}
                topicDescription={topic?.description}
                topicTags={topic?.tags}
              />
            </div>
          </div>
        </div>
      )}
    </>
  )
}