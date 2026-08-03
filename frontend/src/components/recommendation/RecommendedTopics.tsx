import { useCallback, useEffect, useRef, useState, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { TrendingUp, ArrowRight, Info, ChevronLeft, ChevronRight } from 'lucide-react'
import { useRecommendations } from '@/hooks/use-api'
import type { Recommendation } from '@/services/api'

interface RecommendedTopicsProps {
  topicId: number
}

export default function RecommendedTopics({ topicId }: RecommendedTopicsProps) {
  const { data, isLoading } = useRecommendations(topicId)
  const trackRef = useRef<HTMLDivElement>(null)
  const [canScrollLeft, setCanScrollLeft] = useState(false)
  const [canScrollRight, setCanScrollRight] = useState(false)
  const [activeIndex, setActiveIndex] = useState(0)
  const [isHovering, setIsHovering] = useState(false)

  const recommendations = useMemo(() => data?.recommendations || [], [data])

  // ── Scroll position tracking ──────────────────
  const updateScrollState = useCallback(() => {
    const track = trackRef.current
    if (!track) return
    const { scrollLeft, scrollWidth, clientWidth } = track
    setCanScrollLeft(scrollLeft > 4)
    setCanScrollRight(scrollLeft + clientWidth < scrollWidth - 4)
  }, [])

  useEffect(() => {
    const track = trackRef.current
    if (!track) return
    updateScrollState()
    track.addEventListener('scroll', updateScrollState, { passive: true })
    return () => track.removeEventListener('scroll', updateScrollState)
  }, [updateScrollState, recommendations])

  // ── Active dot tracking ───────────────────────
  useEffect(() => {
    const track = trackRef.current
    if (!track || recommendations.length === 0) return

    const onScroll = () => {
      if (!track) return
      const cardWidth = track.querySelector('[data-rec-card]')?.clientWidth ?? 280
      const gap = cardWidth > 0 ? 0 : 0 // no gap in current layout
      const index = Math.round(track.scrollLeft / (cardWidth + gap))
      setActiveIndex(Math.min(index, recommendations.length - 1))
    }

    track.addEventListener('scroll', onScroll, { passive: true })
    // Also recalculate on resize
    window.addEventListener('resize', onScroll)
    onScroll()
    return () => {
      track.removeEventListener('scroll', onScroll)
      window.removeEventListener('resize', onScroll)
    }
  }, [recommendations.length])

  // ── Scroll helpers ────────────────────────────
  const scrollBy = useCallback((direction: 'left' | 'right') => {
    const track = trackRef.current
    if (!track) return
    const cardWidth = track.querySelector('[data-rec-card]')?.clientWidth ?? 280
    const target = track.scrollLeft + (direction === 'left' ? -cardWidth : cardWidth)
    track.scrollTo({ left: target, behavior: 'smooth' })
  }, [])

  const scrollToIndex = useCallback((index: number) => {
    const track = trackRef.current
    if (!track) return
    const cardWidth = track.querySelector('[data-rec-card]')?.clientWidth ?? 280
    track.scrollTo({ left: index * cardWidth, behavior: 'smooth' })
  }, [])

  // ── Keyboard ──────────────────────────────────
  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent) => {
      if (e.key === 'ArrowLeft') {
        e.preventDefault()
        scrollBy('left')
      } else if (e.key === 'ArrowRight') {
        e.preventDefault()
        scrollBy('right')
      }
    },
    [scrollBy]
  )

  // ── Loading state ─────────────────────────────
  if (isLoading) {
    return (
      <div className="border border-[var(--border)] p-8">
        <div className="h-4 w-48 animate-pulse rounded bg-[var(--surface)]" />
        <div className="mt-6 flex gap-0 overflow-hidden">
          {[1, 2, 3].map((i) => (
            <div
              key={i}
              className="h-44 min-w-[280px] flex-shrink-0 animate-pulse border border-[var(--border)] bg-[var(--surface)]"
            />
          ))}
        </div>
      </div>
    )
  }

  if (recommendations.length === 0) return null

  // ── Render ────────────────────────────────────
  return (
    <div
      className="group/carousel relative border border-[var(--border)]"
      onMouseEnter={() => setIsHovering(true)}
      onMouseLeave={() => setIsHovering(false)}
      onKeyDown={handleKeyDown}
      role="region"
      aria-label="Recommended topics"
      tabIndex={0}
    >
      {/* ── Header ─────────────────────────────── */}
      <div className="flex items-center justify-between border-b border-[var(--border)] px-6 py-4">
        <div className="flex items-center gap-3">
          <TrendingUp className="h-5 w-5 text-[var(--accent)]" />
          <h3
            className="font-[var(--font-display)] text-lg text-[var(--fg)]"
            style={{ fontFamily: 'var(--font-display)' }}
          >
            Recommended Topics
          </h3>
        </div>
        <span
          className="font-[var(--font-mono)] text-[0.6875rem] uppercase tracking-[0.1em] text-[var(--muted)]"
          style={{ fontFamily: 'var(--font-mono)' }}
        >
          {recommendations.length} suggestion{recommendations.length !== 1 ? 's' : ''}
        </span>
      </div>

      {/* ── Carousel wrapper ────────────────────── */}
      <div className="relative">
        {/* Gradient fade overlays */}
        <div
          className={`pointer-events-none absolute inset-y-0 left-0 z-10 w-16 bg-gradient-to-r from-[var(--bg)] via-[var(--bg)]/70 to-transparent transition-opacity duration-300 ${
            canScrollLeft ? 'opacity-100' : 'opacity-0'
          }`}
        />
        <div
          className={`pointer-events-none absolute inset-y-0 right-0 z-10 w-16 bg-gradient-to-l from-[var(--bg)] via-[var(--bg)]/70 to-transparent transition-opacity duration-300 ${
            canScrollRight ? 'opacity-100' : 'opacity-0'
          }`}
        />

        {/* Navigation arrows */}
        <button
          type="button"
          onClick={() => scrollBy('left')}
          aria-label="Scroll recommendations left"
          className={`absolute -left-3 top-1/2 z-20 flex h-9 w-9 -translate-y-1/2 items-center justify-center rounded-full border border-[var(--border)] bg-[var(--surface)] text-[var(--muted)] shadow-sm transition-all duration-300 hover:border-[var(--accent)] hover:text-[var(--accent)] hover:shadow-md ${
            canScrollLeft && isHovering ? 'translate-x-0 opacity-100' : '-translate-x-2 opacity-0 pointer-events-none'
          }`}
        >
          <ChevronLeft className="h-4 w-4" />
        </button>

        <button
          type="button"
          onClick={() => scrollBy('right')}
          aria-label="Scroll recommendations right"
          className={`absolute -right-3 top-1/2 z-20 flex h-9 w-9 -translate-y-1/2 items-center justify-center rounded-full border border-[var(--border)] bg-[var(--surface)] text-[var(--muted)] shadow-sm transition-all duration-300 hover:border-[var(--accent)] hover:text-[var(--accent)] hover:shadow-md ${
            canScrollRight && isHovering ? 'translate-x-0 opacity-100' : 'translate-x-2 opacity-0 pointer-events-none'
          }`}
        >
          <ChevronRight className="h-4 w-4" />
        </button>

        {/* ── Scroll track ─────────────────────── */}
        <div
          ref={trackRef}
          className="recommendation-track flex gap-0 overflow-x-auto"
        >
          {recommendations.map((rec: Recommendation, index: number) => (
            <Link
              key={rec.id}
              to={`/topics/${rec.id}`}
              data-rec-card
              className="recommendation-card group/card flex min-w-[280px] max-w-[320px] flex-shrink-0 flex-col border-r border-[var(--border)] p-6 last:border-r-0"
            >
              {/* Numbered indicator */}
              <div className="mb-3 flex items-center justify-between">
                <span
                  className="font-[var(--font-display)] text-2xl text-[var(--border)]"
                  style={{ fontFamily: 'var(--font-display)' }}
                >
                  {(index + 1).toString().padStart(2, '0')}
                </span>
                <ArrowRight className="h-4 w-4 text-[var(--muted)] transition-all duration-300 group-hover/card:translate-x-1 group-hover/card:text-[var(--accent)]" />
              </div>

              {/* Subject name */}
              {rec.subject_name && (
                <span
                  className="font-[var(--font-mono)] text-[0.625rem] uppercase tracking-[0.1em] text-[var(--accent-2)]"
                  style={{ fontFamily: 'var(--font-mono)' }}
                >
                  {rec.subject_name}
                </span>
              )}

              {/* Topic name */}
              <h4
                className="mt-1.5 font-[var(--font-display)] text-base leading-tight text-[var(--fg)] transition-colors duration-300 group-hover/card:text-[var(--accent)]"
                style={{ fontFamily: 'var(--font-display)' }}
              >
                {rec.name}
              </h4>

              {/* Description */}
              {rec.description && (
                <p className="mt-2 text-sm leading-relaxed text-[var(--muted)] line-clamp-2">
                  {rec.description}
                </p>
              )}

              {/* Spacer */}
              <div className="mt-auto" />

              {/* Relevance score bar */}
              <div className="mt-5 flex items-center gap-3 border-t border-[var(--border)] pt-4">
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <span
                      className="font-[var(--font-mono)] text-[0.625rem] uppercase tracking-[0.1em] text-[var(--muted)]"
                      style={{ fontFamily: 'var(--font-mono)' }}
                    >
                      Relevance
                    </span>
                    <div className="h-1 flex-1 overflow-hidden rounded-full bg-[var(--border)]">
                      <div
                        className="h-full rounded-full bg-[var(--accent)] transition-all duration-500"
                        style={{ width: `${rec.relevance_score || 0}%` }}
                      />
                    </div>
                    <span
                      className="font-[var(--font-mono)] text-[0.625rem] text-[var(--accent)] tabular-nums"
                      style={{ fontFamily: 'var(--font-mono)' }}
                    >
                      {rec.relevance_score || 0}%
                    </span>
                  </div>
                </div>
              </div>

              {/* Match reason */}
              {rec.match_reason && (
                <div className="mt-3 flex items-start gap-2">
                  <Info className="mt-0.5 h-3 w-3 flex-shrink-0 text-[var(--muted)]" />
                  <p
                    className="font-[var(--font-mono)] text-[0.5625rem] leading-[1.6] text-[var(--muted)]"
                    style={{ fontFamily: 'var(--font-mono)' }}
                  >
                    {rec.match_reason}
                  </p>
                </div>
              )}

              {/* Tags */}
              {rec.tags && rec.tags.length > 0 && (
                <div className="mt-3 flex flex-wrap gap-1">
                  {rec.tags.slice(0, 2).map((tag: string) => (
                    <span key={tag} className="badge-editorial text-[0.5rem] !px-2 !py-1">
                      {tag}
                    </span>
                  ))}
                </div>
              )}
            </Link>
          ))}
        </div>
      </div>

      {/* ── Progress dots ────────────────────────── */}
      {recommendations.length > 1 && (
        <div className="flex items-center justify-center gap-2 border-t border-[var(--border)] px-6 py-3">
          {recommendations.map((_, index) => (
            <button
              key={index}
              type="button"
              onClick={() => scrollToIndex(index)}
              aria-label={`Go to recommendation ${index + 1}`}
              className={`h-1.5 rounded-full transition-all duration-300 ${
                index === activeIndex
                  ? 'w-6 bg-[var(--accent)]'
                  : 'w-1.5 bg-[var(--border)] hover:bg-[var(--muted)]'
              }`}
            />
          ))}
        </div>
      )}
    </div>
  )
}
