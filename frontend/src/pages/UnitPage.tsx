import { useParams, Link } from 'react-router-dom'
import { ChevronRight, FileText, ArrowRight, BookOpen } from 'lucide-react'
import { useUnit, useUnitTopics } from '@/hooks/use-api'
import type { Topic } from '@/services/api'

export default function UnitPage() {
  const { id } = useParams<{ id: string }>()
  const unitId = Number(id)
  const { data: unit, isLoading } = useUnit(unitId)
  const { data: topics } = useUnitTopics(unitId)

  if (isLoading) {
    return (
      <div className="space-y-8">
        <div className="h-4 w-48 animate-pulse bg-[var(--surface)]" />
        <div className="h-8 w-64 animate-pulse bg-[var(--surface)]" />
        <div className="h-64 animate-pulse border border-[var(--border)] bg-[var(--surface)]" />
      </div>
    )
  }

  if (!unit) {
    return (
      <div className="flex flex-col items-center justify-center py-24">
        <p className="text-[var(--muted)]">Unit not found.</p>
        <Link to="/subjects" className="mt-4 text-[var(--accent)] hover:underline">
          Back to subjects
        </Link>
      </div>
    )
  }

  return (
    <div className="space-y-0">
      {/* Breadcrumb */}
      <nav className="reveal flex items-center gap-2 font-[var(--font-mono)] text-xs uppercase tracking-[0.06em]" style={{ fontFamily: 'var(--font-mono)' }}>
        <Link to="/subjects" className="text-[var(--muted)] transition-colors hover:text-[var(--fg)]">
          Subjects
        </Link>
        <ChevronRight className="h-3 w-3 text-[var(--muted)]" />
        <span className="text-[var(--muted)]">Unit</span>
        <ChevronRight className="h-3 w-3 text-[var(--muted)]" />
        <span className="text-[var(--fg)]">{unit.name}</span>
      </nav>

      {/* Unit Header */}
      <div className="reveal mt-8 border border-[var(--border)] p-[clamp(24px,3vw,40px)]" data-delay="1">
        <div className="flex items-center gap-3">
          <span className="flex h-12 w-12 items-center justify-center border border-[var(--accent)] font-[var(--font-mono)] text-xl text-[var(--accent)]" style={{ fontFamily: 'var(--font-mono)' }}>
            {unit.number}
          </span>
          <div>
            <p className="font-[var(--font-mono)] text-[0.6875rem] uppercase tracking-[0.1em] text-[var(--accent-2)]" style={{ fontFamily: 'var(--font-mono)' }}>
              Unit {unit.number}
            </p>
            <h1 className="mt-2 font-[var(--font-display)] text-[clamp(2rem,4vw,3.5rem)] leading-[1.12] tracking-[-0.015em] text-[var(--fg)]" style={{ fontFamily: 'var(--font-display)' }}>
              {unit.name}
            </h1>
          </div>
        </div>
        {unit.description && (
          <p className="mt-6 max-w-[680px] text-[clamp(1rem,1.3vw,1.125rem)] leading-[1.8] text-[var(--muted)]">
            {unit.description}
          </p>
        )}
        <div className="mt-6 flex items-center gap-4">
          <span className="font-[var(--font-mono)] text-xs uppercase tracking-[0.06em] text-[var(--accent)]" style={{ fontFamily: 'var(--font-mono)' }}>
            {topics?.length || 0} Topics
          </span>
        </div>
      </div>

      {/* Topics */}
      <section className="reveal mt-12 border-t border-[var(--border)] pt-12" data-delay="2">
        <p className="font-[var(--font-mono)] text-[clamp(0.6875rem,0.9vw,0.75rem)] uppercase tracking-[0.14em] text-[var(--accent)]" style={{ fontFamily: 'var(--font-mono)' }}>
          Topics
        </p>
        <h2 className="mt-4 font-[var(--font-display)] text-[clamp(1.5rem,3vw,2.5rem)] leading-[1.12] text-[var(--fg)]" style={{ fontFamily: 'var(--font-display)' }}>
          Select a topic to learn
        </h2>

        {topics && topics.length > 0 ? (
          <div className="mt-8 grid grid-cols-1 gap-0 sm:grid-cols-2">
            {topics.map((topic: Topic, index: number) => (
              <Link
                key={topic.id}
                to={`/topics/${topic.id}`}
                className="reveal group border border-[var(--border)] p-[clamp(24px,3vw,40px)] transition-all hover:bg-[var(--surface)]"
                data-delay={Math.min(index + 1, 5).toString()}
              >
                <div className="flex items-start justify-between">
                  <div>
                    <h3 className="font-[var(--font-display)] text-[clamp(1.25rem,2vw,1.75rem)] text-[var(--fg)] transition-colors group-hover:text-[var(--accent)]" style={{ fontFamily: 'var(--font-display)' }}>
                      {topic.name}
                    </h3>
                    {topic.description && (
                      <p className="mt-3 text-sm leading-[1.6] text-[var(--muted)] line-clamp-2">
                        {topic.description}
                      </p>
                    )}
                    {topic.tags && topic.tags.length > 0 && (
                      <div className="mt-4 flex flex-wrap gap-1">
                        {topic.tags.slice(0, 3).map((tag: string) => (
                          <span key={tag} className="badge-editorial text-[0.5625rem]">
                            {tag}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                  <ArrowRight className="h-5 w-5 flex-shrink-0 text-[var(--muted)] transition-all group-hover:translate-x-1 group-hover:text-[var(--accent)]" />
                </div>
                <div className="mt-6 flex items-center gap-4 border-t border-[var(--border)] pt-4">
                  {topic.importance_score !== undefined && (
                    <div className="flex items-center gap-2">
                      <span className="font-[var(--font-mono)] text-[0.625rem] uppercase tracking-[0.1em] text-[var(--muted)]" style={{ fontFamily: 'var(--font-mono)' }}>
                        Importance
                      </span>
                      <div className="h-1 w-16 bg-[var(--border)]">
                        <div
                          className="h-full bg-[var(--accent)]"
                          style={{ width: `${(topic.importance_score || 0) * 100}%` }}
                        />
                      </div>
                      <span className="font-[var(--font-mono)] text-[0.625rem] text-[var(--accent)]" style={{ fontFamily: 'var(--font-mono)' }}>
                        {Math.round((topic.importance_score || 0) * 100)}%
                      </span>
                    </div>
                  )}
                  <span className="font-[var(--font-mono)] text-[0.625rem] uppercase tracking-[0.1em] text-[var(--muted)]" style={{ fontFamily: 'var(--font-mono)' }}>
                    {topic.resource_count || 0} Resources
                  </span>
                </div>
              </Link>
            ))}
          </div>
        ) : (
          <div className="mt-8 flex flex-col items-center justify-center py-16 text-center">
            <FileText className="h-16 w-16 text-[var(--muted)] opacity-30" />
            <p className="mt-6 text-[var(--muted)]">No topics available</p>
          </div>
        )}
      </section>
    </div>
  )
}
