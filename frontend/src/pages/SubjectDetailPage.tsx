import { useParams, Link } from 'react-router-dom'
import { ChevronRight, BookOpen, ArrowRight, Layers } from 'lucide-react'
import { useSubject, useSubjectUnits } from '@/hooks/use-api'
import type { Unit } from '@/services/api'

export default function SubjectDetailPage() {
  const { id } = useParams<{ id: string }>()
  const subjectId = Number(id)
  const { data: subject, isLoading } = useSubject(subjectId)
  const { data: units } = useSubjectUnits(subjectId)

  if (isLoading) {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
        <div style={{ height: '16px', width: '200px', background: 'var(--surface)', borderRadius: 'var(--radius)' }} />
        <div style={{ height: '32px', width: '300px', background: 'var(--surface)', borderRadius: 'var(--radius)' }} />
        <div style={{ height: '200px', background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 'var(--radius)' }} />
      </div>
    )
  }

  if (!subject) {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '96px 0' }}>
        <p style={{ color: 'var(--muted)' }}>Subject not found.</p>
        <Link to="/subjects" style={{ marginTop: '16px', color: 'var(--accent)' }}>
          Back to subjects
        </Link>
      </div>
    )
  }

  return (
    <div>
      {/* Breadcrumb */}
      <nav
        className="reveal"
        style={{ display: 'flex', alignItems: 'center', gap: '8px', fontFamily: 'var(--font-mono)', fontSize: '12px', textTransform: 'uppercase', letterSpacing: '0.06em' }}
      >
        <Link to="/subjects" style={{ color: 'var(--muted)', textDecoration: 'none' }}>Subjects</Link>
        <ChevronRight style={{ width: '12px', height: '12px', color: 'var(--muted)' }} />
        <span style={{ color: 'var(--fg)' }}>{subject.name}</span>
      </nav>

      {/* Subject Header Card */}
      <div
        className="reveal"
        data-delay="1"
        style={{
          marginTop: '32px',
          border: '1px solid var(--border)',
          borderRadius: 'var(--radius)',
          padding: 'clamp(24px, 3vw, 40px)',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'flex-start', gap: '24px', flexWrap: 'wrap' }}>
          <div
            style={{
              width: '64px',
              height: '64px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              border: '1px solid var(--border)',
              borderRadius: 'var(--radius)',
              flexShrink: 0,
            }}
          >
            <BookOpen style={{ width: '32px', height: '32px', color: 'var(--accent)' }} />
          </div>
          <div style={{ flex: 1 }}>
            <span className="badge-editorial">{subject.code}</span>
            <h1 style={{ fontFamily: 'var(--font-display)', fontSize: 'clamp(2rem, 4vw, 3rem)', lineHeight: 1.12, color: 'var(--fg)', marginTop: '16px' }}>
              {subject.name}
            </h1>
            {subject.description && (
              <p style={{ maxWidth: '680px', fontSize: 'clamp(1rem, 1.3vw, 1.1rem)', lineHeight: 1.8, color: 'var(--muted)', marginTop: '20px' }}>
                {subject.description}
              </p>
            )}
            {subject.tags && subject.tags.length > 0 && (
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginTop: '20px' }}>
                {subject.tags.map((tag: string) => (
                  <span key={tag} className="badge-editorial">{tag}</span>
                ))}
              </div>
            )}
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginTop: '20px' }}>
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: '12px', textTransform: 'uppercase', letterSpacing: '0.06em', color: 'var(--muted)' }}>
                Semester {subject.semester_number || '?'}
              </span>
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: '12px', textTransform: 'uppercase', letterSpacing: '0.06em', color: 'var(--accent)' }}>
                {units?.length || 0} Units
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Units */}
      <section className="reveal" data-delay="2" style={{ marginTop: '48px', paddingTop: '48px', borderTop: '1px solid var(--border)' }}>
        <p style={{ fontFamily: 'var(--font-mono)', fontSize: '12px', textTransform: 'uppercase', letterSpacing: '0.14em', color: 'var(--accent)' }}>
          Units
        </p>
        <h2 style={{ fontFamily: 'var(--font-display)', fontSize: 'clamp(1.5rem, 3vw, 2.25rem)', lineHeight: 1.12, color: 'var(--fg)', marginTop: '16px' }}>
          Select a unit to explore
        </h2>

        {units && units.length > 0 ? (
          <div
            style={{
              marginTop: '32px',
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
              gap: '20px',
            }}
          >
            {units.map((unit: Unit, index: number) => (
              <Link
                key={unit.id}
                to={`/units/${unit.id}`}
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
                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                      <span
                        style={{
                          display: 'flex',
                          width: '32px',
                          height: '32px',
                          alignItems: 'center',
                          justifyContent: 'center',
                          border: '1px solid var(--accent)',
                          borderRadius: 'var(--radius)',
                          fontFamily: 'var(--font-mono)',
                          fontSize: '14px',
                          color: 'var(--accent)',
                        }}
                      >
                        {unit.number}
                      </span>
                      <span style={{ fontFamily: 'var(--font-mono)', fontSize: '10px', textTransform: 'uppercase', letterSpacing: '0.1em', color: 'var(--muted)' }}>
                        Unit {unit.number}
                      </span>
                    </div>
                    <h3 style={{ fontFamily: 'var(--font-display)', fontSize: 'clamp(1.2rem, 2vw, 1.5rem)', color: 'var(--fg)', marginTop: '16px' }}>
                      {unit.name}
                    </h3>
                    {unit.description && (
                      <p style={{ fontSize: '14px', lineHeight: 1.6, color: 'var(--muted)', marginTop: '12px', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                        {unit.description}
                      </p>
                    )}
                  </div>
                  <ArrowRight style={{ width: '20px', height: '20px', flexShrink: 0, color: 'var(--muted)' }} />
                </div>
                <div style={{ marginTop: '20px', paddingTop: '16px', borderTop: '1px solid var(--border)', display: 'flex', alignItems: 'center', gap: '16px' }}>
                  <span style={{ fontFamily: 'var(--font-mono)', fontSize: '10px', textTransform: 'uppercase', letterSpacing: '0.1em', color: 'var(--accent)' }}>
                    {unit.topics_count || 0} Topics
                  </span>
                  <span style={{ fontFamily: 'var(--font-mono)', fontSize: '10px', textTransform: 'uppercase', letterSpacing: '0.1em', color: 'var(--muted)' }}>
                    View Topics →
                  </span>
                </div>
              </Link>
            ))}
          </div>
        ) : (
          <div style={{ marginTop: '32px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '64px 0', textAlign: 'center' }}>
            <Layers style={{ width: '64px', height: '64px', color: 'var(--muted)', opacity: 0.3 }} />
            <p style={{ color: 'var(--muted)', marginTop: '24px' }}>No units available</p>
          </div>
        )}
      </section>
    </div>
  )
}
