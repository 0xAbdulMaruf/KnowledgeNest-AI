import { GraduationCap } from 'lucide-react'

export default function Preloader() {
  return (
    <div className="fixed inset-0 z-[9999] flex flex-col items-center justify-center bg-[var(--bg)]">
      <div className="relative">
        <GraduationCap className="h-12 w-12 animate-pulse text-[var(--accent)]" />
        <div className="absolute -bottom-3 left-1/2 h-1 w-12 -translate-x-1/2 overflow-hidden rounded-full bg-[var(--border)]">
          <div
            className="h-full animate-[slideRight_1.5s_ease-in-out_infinite] rounded-full bg-[var(--accent)]"
            style={{ width: '40%' }}
          />
        </div>
      </div>
      <p
        className="mt-8 font-[var(--font-display)] text-lg tracking-tight text-[var(--fg)]"
        style={{ fontFamily: 'var(--font-display)' }}
      >
        KnowledgeNest AI
      </p>
      <p
        className="mt-2 font-[var(--font-mono)] text-xs uppercase tracking-[0.14em] text-[var(--muted)]"
        style={{ fontFamily: 'var(--font-mono)' }}
      >
        Loading...
      </p>
    </div>
  )
}
