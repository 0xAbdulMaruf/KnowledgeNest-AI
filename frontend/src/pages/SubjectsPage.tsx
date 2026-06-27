import { useState } from 'react'
import { Link } from 'react-router-dom'
import { BookOpen, ArrowRight, Filter } from 'lucide-react'
import { useSubjects, useSemesters } from '@/hooks/use-api'

export default function SubjectsPage() {
  const [selectedSemester, setSelectedSemester] = useState<number | undefined>()
  const { data: semesters } = useSemesters()
  const { data: subjects, isLoading } = useSubjects(selectedSemester)

  const getSemesterNumber = (semesterId: number) => {
    const sem = semesters?.find((s) => s.id === semesterId)
    return sem ? sem.number : '?'
  }

  return (
    <div>
      {/* Header */}
      <section style={{ borderBottom: '1px solid var(--border)', paddingBottom: '48px', paddingTop: '16px' }}>
        <p
          className="reveal"
          style={{ fontFamily: 'var(--font-mono)', fontSize: '12px', textTransform: 'uppercase', letterSpacing: '0.12em', color: 'var(--accent)' }}
        >
          Browse
        </p>
        <h1
          className="reveal"
          data-delay="1"
          style={{ fontFamily: 'var(--font-display)', fontSize: 'clamp(2.5rem, 5vw, 4rem)', lineHeight: 1.1, color: 'var(--fg)', marginTop: '16px' }}
        >
          Subjects
        </h1>
        <p
          className="reveal"
          data-delay="2"
          style={{ maxWidth: '54ch', fontSize: 'clamp(1rem, 1.5vw, 1.2rem)', lineHeight: 1.7, color: 'var(--muted)', marginTop: '16px' }}
        >
          Explore all subjects across semesters. Select a semester to filter.
        </p>
      </section>

      {/* Semester Filter */}
      <section className="reveal" data-delay="3" style={{ borderTop: '1px solid var(--border)', padding: '24px 0' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', overflowX: 'auto' }}>
          <span style={{ display: 'flex', alignItems: 'center', gap: '8px', fontFamily: 'var(--font-mono)', fontSize: '12px', textTransform: 'uppercase', letterSpacing: '0.06em', color: 'var(--muted)' }}>
            <Filter style={{ width: '16px', height: '16px' }} />
            Filter
          </span>
          <button
            onClick={() => setSelectedSemester(undefined)}
            style={{
              whiteSpace: 'nowrap',
              padding: '8px 16px',
              fontSize: '14px',
              borderRadius: 'var(--radius)',
              border: `1px solid ${!selectedSemester ? 'var(--accent)' : 'var(--border)'}`,
              background: !selectedSemester ? 'var(--accent)' : 'transparent',
              color: !selectedSemester ? '#fff' : 'var(--muted)',
              cursor: 'pointer',
              transition: 'all 0.2s ease',
            }}
          >
            All Semesters
          </button>
          {semesters?.map((semester) => (
            <button
              key={semester.id}
              onClick={() => setSelectedSemester(semester.id)}
              style={{
                whiteSpace: 'nowrap',
                padding: '8px 16px',
                fontSize: '14px',
                borderRadius: 'var(--radius)',
                border: `1px solid ${selectedSemester === semester.id ? 'var(--accent)' : 'var(--border)'}`,
                background: selectedSemester === semester.id ? 'var(--accent)' : 'transparent',
                color: selectedSemester === semester.id ? '#fff' : 'var(--muted)',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
              }}
            >
              Semester {semester.number}
            </button>
          ))}
        </div>
      </section>

      {/* Subjects Grid */}
      <section style={{ paddingTop: '48px', paddingBottom: '80px' }}>
        {isLoading ? (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '20px' }}>
            {Array.from({ length: 6 }).map((_, i) => (
              <div
                key={i}
                style={{ height: '200px', border: '1px solid var(--border)', borderRadius: 'var(--radius)', background: 'var(--surface)' }}
              />
            ))}
          </div>
        ) : subjects && subjects.length > 0 ? (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '20px' }}>
            {subjects.map((subject: any, index: number) => (
              <Link
                key={subject.id}
                to={`/subjects/${subject.id}`}
                className="reveal card-hover"
                data-delay={Math.min(index + 1, 5).toString()}
                style={{
                  display: 'block',
                  padding: 'clamp(20px, 3vw, 36px)',
                  border: '1px solid var(--border)',
                  borderRadius: 'var(--radius)',
                  textDecoration: 'none',
                  background: 'var(--bg)',
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <div style={{ flex: 1 }}>
                    <span className="badge-editorial">{subject.code}</span>
                    <h3 style={{ fontFamily: 'var(--font-display)', fontSize: 'clamp(1.2rem, 2vw, 1.6rem)', color: 'var(--fg)', marginTop: '16px' }}>
                      {subject.name}
                    </h3>
                    {subject.description && (
                      <p style={{ fontSize: '14px', lineHeight: 1.6, color: 'var(--muted)', marginTop: '12px', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                        {subject.description}
                      </p>
                    )}
                    {subject.tags && subject.tags.length > 0 && (
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', marginTop: '16px' }}>
                        {subject.tags.slice(0, 3).map((tag: string) => (
                          <span key={tag} className="badge-editorial" style={{ fontSize: '10px' }}>
                            {tag}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                  <ArrowRight style={{ width: '20px', height: '20px', flexShrink: 0, color: 'var(--muted)' }} />
                </div>
                <div style={{ marginTop: '20px', paddingTop: '16px', borderTop: '1px solid var(--border)', display: 'flex', alignItems: 'center', gap: '16px' }}>
                  <span style={{ fontFamily: 'var(--font-mono)', fontSize: '10px', textTransform: 'uppercase', letterSpacing: '0.1em', color: 'var(--muted)' }}>
                    Semester {getSemesterNumber(subject.semester_id)}
                  </span>
                  <span style={{ fontFamily: 'var(--font-mono)', fontSize: '10px', textTransform: 'uppercase', letterSpacing: '0.1em', color: 'var(--accent)' }}>
                    View Units →
                  </span>
                </div>
              </Link>
            ))}
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '64px 0', textAlign: 'center' }}>
            <BookOpen style={{ width: '64px', height: '64px', color: 'var(--muted)', opacity: 0.3 }} />
            <p style={{ color: 'var(--muted)', marginTop: '24px' }}>No subjects found</p>
            <p style={{ color: 'var(--muted)', fontSize: '14px', marginTop: '8px' }}>Try selecting a different semester</p>
          </div>
        )}
      </section>
    </div>
  )
}
