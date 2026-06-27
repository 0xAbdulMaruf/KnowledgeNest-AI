import { useState, useEffect } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { Search, BookOpen, FileText, Layers, ArrowRight, TrendingUp } from 'lucide-react'
import { useSearch } from '@/hooks/use-api'

export default function SearchPage() {
  const [searchParams] = useSearchParams()
  const query = searchParams.get('q') || ''
  const [inputValue, setInputValue] = useState(query)

  useEffect(() => {
    setInputValue(query)
  }, [query])

  const { data, isLoading } = useSearch(query)

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    if (inputValue.trim()) {
      window.location.href = `/search?q=${encodeURIComponent(inputValue.trim())}`
    }
  }

  return (
    <div className="space-y-0">
      {/* Search Header */}
      <section className="border-b border-[var(--border)] pb-12 pt-8">
        <p className="reveal font-[var(--font-mono)] text-xs uppercase tracking-[0.12em] text-[var(--accent)]" style={{ fontFamily: 'var(--font-mono)' }}>
          Search
        </p>
        <h1 className="reveal mt-4 font-[var(--font-display)] text-[clamp(2.5rem,5vw,4rem)] leading-[1.1] tracking-[-0.02em] text-[var(--fg)]" data-delay="1" style={{ fontFamily: 'var(--font-display)' }}>
          Find what you need
        </h1>

        <form onSubmit={handleSearch} className="reveal mt-8" data-delay="2">
          <div className="flex items-center gap-0 border border-[var(--border)]">
            <div className="flex items-center gap-3 px-4 py-3">
              <Search className="h-5 w-5 text-[var(--muted)]" />
            </div>
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Search topics, subjects, units, PYQs..."
              className="flex-1 bg-transparent py-3 pr-4 text-lg text-[var(--fg)] placeholder-[var(--muted)] outline-none"
            />
            <button
              type="submit"
              className="bg-[var(--accent)] px-6 py-3 text-sm font-semibold text-[var(--bg)] transition-opacity hover:opacity-90"
            >
              Search
            </button>
          </div>
        </form>
      </section>

      {/* Results */}
      {query && (
        <section className="border-t border-[var(--border)] py-[clamp(64px,10vh,140px)]">
          <div className="reveal">
            <p className="font-[var(--font-mono)] text-[clamp(0.6875rem,0.9vw,0.75rem)] uppercase tracking-[0.14em] text-[var(--accent)]" style={{ fontFamily: 'var(--font-mono)' }}>
              Results for "{query}"
            </p>
            <h2 className="mt-4 font-[var(--font-display)] text-[clamp(1.5rem,3vw,2.5rem)] leading-[1.12] text-[var(--fg)]" style={{ fontFamily: 'var(--font-display)' }}>
              {data?.total_results || 0} results found
            </h2>
          </div>

          {isLoading ? (
            <div className="mt-12 grid grid-cols-1 gap-0 sm:grid-cols-2">
              {Array.from({ length: 4 }).map((_, i) => (
                <div key={i} className="h-32 animate-pulse border border-[var(--border)] bg-[var(--surface)]" />
              ))}
            </div>
          ) : data && (data.total_results || 0) > 0 ? (
            <div className="mt-12 space-y-12">
              {/* Subjects */}
              {data.subjects && data.subjects.length > 0 && (
                <div>
                  <h3 className="flex items-center gap-2 font-[var(--font-mono)] text-xs uppercase tracking-[0.1em] text-[var(--muted)]" style={{ fontFamily: 'var(--font-mono)' }}>
                    <BookOpen className="h-4 w-4" />
                    Subjects
                  </h3>
                  <div className="mt-4 grid grid-cols-1 gap-0 sm:grid-cols-2">
                    {data.subjects.map((subject: any) => (
                      <Link
                        key={subject.id}
                        to={`/subjects/${subject.id}`}
                        className="group border border-[var(--border)] p-6 transition-all hover:bg-[var(--surface)]"
                      >
                        <div className="flex items-center justify-between">
                          <div>
                            <span className="badge-editorial">{subject.code}</span>
                            <h4 className="mt-3 font-[var(--font-display)] text-lg text-[var(--fg)] transition-colors group-hover:text-[var(--accent)]" style={{ fontFamily: 'var(--font-display)' }}>
                              {subject.name}
                            </h4>
                            <p className="mt-2 text-sm text-[var(--muted)] line-clamp-2">
                              {subject.description}
                            </p>
                          </div>
                          <ArrowRight className="h-5 w-5 text-[var(--muted)] transition-all group-hover:translate-x-1 group-hover:text-[var(--accent)]" />
                        </div>
                      </Link>
                    ))}
                  </div>
                </div>
              )}

              {/* Topics */}
              {data.topics && data.topics.length > 0 && (
                <div>
                  <h3 className="flex items-center gap-2 font-[var(--font-mono)] text-xs uppercase tracking-[0.1em] text-[var(--muted)]" style={{ fontFamily: 'var(--font-mono)' }}>
                    <FileText className="h-4 w-4" />
                    Topics
                  </h3>
                  <div className="mt-4 grid grid-cols-1 gap-0 sm:grid-cols-2">
                    {data.topics.map((topic: any) => (
                      <Link
                        key={topic.id}
                        to={`/topics/${topic.id}`}
                        className="group border border-[var(--border)] p-6 transition-all hover:bg-[var(--surface)]"
                      >
                        <div className="flex items-center justify-between">
                          <div>
                            {topic.subject_name && (
                              <span className="font-[var(--font-mono)] text-[0.625rem] uppercase tracking-[0.1em] text-[var(--accent-2)]" style={{ fontFamily: 'var(--font-mono)' }}>
                                {topic.subject_name}
                              </span>
                            )}
                            <h4 className="mt-2 font-[var(--font-display)] text-lg text-[var(--fg)] transition-colors group-hover:text-[var(--accent)]" style={{ fontFamily: 'var(--font-display)' }}>
                              {topic.name}
                            </h4>
                            <p className="mt-2 text-sm text-[var(--muted)] line-clamp-2">
                              {topic.description}
                            </p>
                            {topic.tags && topic.tags.length > 0 && (
                              <div className="mt-3 flex flex-wrap gap-1">
                                {topic.tags.slice(0, 3).map((tag: string) => (
                                  <span key={tag} className="badge-editorial text-[0.5625rem]">
                                    {tag}
                                  </span>
                                ))}
                              </div>
                            )}
                          </div>
                          <ArrowRight className="h-5 w-5 text-[var(--muted)] transition-all group-hover:translate-x-1 group-hover:text-[var(--accent)]" />
                        </div>
                      </Link>
                    ))}
                  </div>
                </div>
              )}

              {/* Units */}
              {data.units && data.units.length > 0 && (
                <div>
                  <h3 className="flex items-center gap-2 font-[var(--font-mono)] text-xs uppercase tracking-[0.1em] text-[var(--muted)]" style={{ fontFamily: 'var(--font-mono)' }}>
                    <Layers className="h-4 w-4" />
                    Units
                  </h3>
                  <div className="mt-4 grid grid-cols-1 gap-0 sm:grid-cols-2">
                    {data.units.map((unit: any) => (
                      <Link
                        key={unit.id}
                        to={`/units/${unit.id}`}
                        className="group border border-[var(--border)] p-6 transition-all hover:bg-[var(--surface)]"
                      >
                        <div className="flex items-center justify-between">
                          <div>
                            {unit.subject_name && (
                              <span className="font-[var(--font-mono)] text-[0.625rem] uppercase tracking-[0.1em] text-[var(--accent-2)]" style={{ fontFamily: 'var(--font-mono)' }}>
                                {unit.subject_name}
                              </span>
                            )}
                            <h4 className="mt-2 font-[var(--font-display)] text-lg text-[var(--fg)] transition-colors group-hover:text-[var(--accent)]" style={{ fontFamily: 'var(--font-display)' }}>
                              {unit.name}
                            </h4>
                          </div>
                          <ArrowRight className="h-5 w-5 text-[var(--muted)] transition-all group-hover:translate-x-1 group-hover:text-[var(--accent)]" />
                        </div>
                      </Link>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="mt-12 flex flex-col items-center justify-center py-16 text-center">
              <Search className="h-16 w-16 text-[var(--muted)] opacity-30" />
              <p className="mt-6 text-[var(--muted)]">No results found for "{query}"</p>
              <p className="mt-2 text-sm text-[var(--muted)]">Try different keywords or browse subjects</p>
            </div>
          )}
        </section>
      )}

      {/* No query state */}
      {!query && (
        <section className="border-t border-[var(--border)] py-[clamp(64px,10vh,140px)]">
          <div className="flex flex-col items-center justify-center py-16 text-center">
            <TrendingUp className="h-16 w-16 text-[var(--muted)] opacity-30" />
            <p className="mt-6 text-[var(--muted)]">Enter a search term to find topics</p>
            <p className="mt-2 text-sm text-[var(--muted)]">Try "python", "pointers", "loops", or "array"</p>
          </div>
        </section>
      )}
    </div>
  )
}
