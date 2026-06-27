import { Link } from 'react-router-dom'
import { TrendingUp, ArrowRight, Info } from 'lucide-react'
import { useRecommendations } from '@/hooks/use-api'

interface RecommendedTopicsProps {
  topicId: number
}

export default function RecommendedTopics({ topicId }: RecommendedTopicsProps) {
  const { data, isLoading } = useRecommendations(topicId)

  if (isLoading) {
    return (
      <div className="border border-[var(--border)] p-8">
        <div className="h-4 w-48 animate-pulse bg-[var(--surface)]" />
        <div className="mt-6 flex gap-0 overflow-hidden">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-40 min-w-[280px] animate-pulse border border-[var(--border)] bg-[var(--surface)]" />
          ))}
        </div>
      </div>
    )
  }

  const recommendations = data?.recommendations || []
  if (!data || recommendations.length === 0) {
    return null
  }

  return (
    <div className="border border-[var(--border)]">
      <div className="flex items-center justify-between border-b border-[var(--border)] px-6 py-4">
        <div className="flex items-center gap-3">
          <TrendingUp className="h-5 w-5 text-[var(--accent)]" />
          <h3 className="font-[var(--font-display)] text-lg text-[var(--fg)]" style={{ fontFamily: 'var(--font-display)' }}>
            Recommended Topics
          </h3>
        </div>
        <span className="font-[var(--font-mono)] text-[0.6875rem] uppercase tracking-[0.1em] text-[var(--muted)]" style={{ fontFamily: 'var(--font-mono)' }}>
          {recommendations.length} suggestions
        </span>
      </div>

      <div className="overflow-x-auto">
        <div className="flex gap-0 p-0">
          {recommendations.map((rec: any, index: number) => (
            <Link
              key={rec.id}
              to={`/topics/${rec.id}`}
              className="group flex min-w-[280px] flex-col border-r border-[var(--border)] p-6 transition-all last:border-r-0 hover:bg-[var(--surface)]"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  {rec.subject_name && (
                    <span className="font-[var(--font-mono)] text-[0.625rem] uppercase tracking-[0.1em] text-[var(--accent-2)]" style={{ fontFamily: 'var(--font-mono)' }}>
                      {rec.subject_name}
                    </span>
                  )}
                  <h4 className="mt-2 font-[var(--font-display)] text-base text-[var(--fg)] transition-colors group-hover:text-[var(--accent)]" style={{ fontFamily: 'var(--font-display)' }}>
                    {rec.name}
                  </h4>
                  {rec.description && (
                    <p className="mt-2 text-sm text-[var(--muted)] line-clamp-2">
                      {rec.description}
                    </p>
                  )}
                </div>
                <ArrowRight className="h-4 w-4 flex-shrink-0 text-[var(--muted)] transition-all group-hover:translate-x-1 group-hover:text-[var(--accent)]" />
              </div>

              {/* Relevance Score */}
              <div className="mt-4 flex items-center gap-3 border-t border-[var(--border)] pt-4">
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <span className="font-[var(--font-mono)] text-[0.625rem] uppercase tracking-[0.1em] text-[var(--muted)]" style={{ fontFamily: 'var(--font-mono)' }}>
                      Relevance
                    </span>
                    <div className="h-1 flex-1 bg-[var(--border)]">
                      <div
                        className="h-full bg-[var(--accent)]"
                        style={{ width: `${rec.relevance_score || 0}%` }}
                      />
                    </div>
                    <span className="font-[var(--font-mono)] text-[0.625rem] text-[var(--accent)]" style={{ fontFamily: 'var(--font-mono)' }}>
                      {rec.relevance_score || 0}%
                    </span>
                  </div>
                </div>
              </div>

              {/* Match Reason */}
              {rec.match_reason && (
                <div className="mt-3 flex items-start gap-2">
                  <Info className="mt-0.5 h-3 w-3 flex-shrink-0 text-[var(--muted)]" />
                  <p className="font-[var(--font-mono)] text-[0.5625rem] leading-[1.6] text-[var(--muted)]" style={{ fontFamily: 'var(--font-mono)' }}>
                    {rec.match_reason}
                  </p>
                </div>
              )}

              {/* Tags */}
              {rec.tags && rec.tags.length > 0 && (
                <div className="mt-3 flex flex-wrap gap-1">
                  {rec.tags.slice(0, 2).map((tag: string) => (
                    <span key={tag} className="badge-editorial text-[0.5rem]">
                      {tag}
                    </span>
                  ))}
                </div>
              )}
            </Link>
          ))}
        </div>
      </div>
    </div>
  )
}
