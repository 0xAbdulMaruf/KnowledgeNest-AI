import { useEffect, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import { BookOpen, ArrowRight, TrendingUp, GraduationCap } from 'lucide-react'
import { useSemesters } from '@/hooks/use-api'
import SearchBar from '@/components/search/SearchBar'

/* ── Animated Counter ─────────────────────── */
function AnimatedStat({
  target,
  label,
  sub,
  delay,
}: {
  target: string
  label: string
  sub: string
  delay: number
}) {
  const ref = useRef<HTMLDivElement>(null)
  const [visible, setVisible] = useState(false)
  const [count, setCount] = useState(0)

  // If the value is not purely numeric (e.g. "24/7"), just display it directly
  const isNumeric = /^\d+$/.test(target)
  const targetNum = isNumeric ? parseInt(target, 10) : 0

  useEffect(() => {
    const el = ref.current
    if (!el) return
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setVisible(true)
          observer.disconnect()
        }
      },
      { threshold: 0.3 }
    )
    observer.observe(el)
    return () => observer.disconnect()
  }, [])

  useEffect(() => {
    if (!visible || !isNumeric) return
    const duration = 1400
    const start = performance.now()
    const animate = (now: number) => {
      const elapsed = now - start
      const progress = Math.min(elapsed / duration, 1)
      // easeOutExpo
      const eased = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress)
      setCount(Math.round(eased * targetNum))
      if (progress < 1) requestAnimationFrame(animate)
    }
    const id = requestAnimationFrame(animate)
    return () => cancelAnimationFrame(id)
  }, [visible, isNumeric, targetNum])

  return (
    <div
      ref={ref}
      className={`stat-card-animated ${visible ? 'stat-visible' : ''}`}
      data-delay={delay.toString()}
      style={{
        textAlign: 'center',
        padding: 'clamp(24px, 3vw, 36px)',
        border: '1px solid var(--border)',
        borderRadius: 'var(--radius)',
      }}
    >
      <p className="metric__value">{isNumeric ? count.toLocaleString() : target}</p>
      <p style={{ fontSize: '14px', color: 'var(--fg)', marginTop: '12px' }}>{label}</p>
      <p
        style={{
          fontFamily: 'var(--font-mono)',
          fontSize: '11px',
          color: 'var(--muted)',
          marginTop: '4px',
        }}
      >
        {sub}
      </p>
    </div>
  )
}

/* ── Page ──────────────────────────────────── */
export default function HomePage() {
  const { data: semesters, isLoading } = useSemesters()

  return (
    <div>
      {/* ── Hero Section ──────────────────────── */}
      <section
        className="reveal"
        style={{
          position: 'relative',
          zIndex: 10,
          display: 'grid',
          gridTemplateColumns: '1fr',
          gap: '48px',
          alignItems: 'center',
          minHeight: '60vh',
          paddingTop: '40px',
          paddingBottom: '64px',
        }}
      >
        {/* Two-column on desktop */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))',
            gap: '48px',
            alignItems: 'center',
          }}
        >
          {/* Left: Text */}
          <div>
            <p
              className="reveal"
              style={{
                fontFamily: 'var(--font-mono)',
                fontSize: '12px',
                textTransform: 'uppercase',
                letterSpacing: '0.12em',
                color: 'var(--accent)',
              }}
            >
              KnowledgeNest AI — Safe & Smart Learning
            </p>
            <h1
              className="reveal hero-title-animated"
              data-delay="1"
              style={{
                fontFamily: 'var(--font-display)',
                fontSize: 'clamp(2.25rem, 5vw, 4rem)',
                lineHeight: 1.1,
                letterSpacing: '-0.02em',
                marginTop: '20px',
              }}
            >
              AI-powered academic resource nest
            </h1>
            <p
              className="reveal"
              data-delay="2"
              style={{
                maxWidth: '50ch',
                fontSize: 'clamp(1rem, 1.3vw, 1.15rem)',
                lineHeight: 1.65,
                color: 'var(--muted)',
                marginTop: '20px',
              }}
            >
              Explore curated academic subjects, view syllabus topics, download premium study
              materials, and access AI assistant recommendations.
            </p>
            <div
              className="reveal search-pulse"
              data-delay="3"
              style={{ marginTop: '28px', maxWidth: '540px' }}
            >
              <SearchBar size="lg" />
            </div>
          </div>

          {/* Right: Hero image */}
          <div
            className="reveal hero-image-float"
            data-delay="2"
            style={{
              overflow: 'hidden',
              border: '1px solid var(--border)',
              background: 'var(--surface)',
              borderRadius: 'var(--radius)',
              padding: '8px',
            }}
          >
            <img
              src="/hero.png"
              alt="KnowledgeNest AI"
              style={{
                width: '100%',
                height: 'auto',
                objectFit: 'cover',
                aspectRatio: '1 / 1',
                borderRadius: 'calc(var(--radius) - 4px)',
                display: 'block',
              }}
            />
          </div>
        </div>
      </section>

      {/* ── Ticker ────────────────────────────── */}
      <div className="ticker">
        <div className="ticker__track">
          {[
            'Data Structures · Notes',
            'Python · Programming',
            'C Language · Fundamentals',
            'Algorithms · Problem Solving',
            'PYQs · Previous Papers',
            'AI Assistant · Smart Help',
            'Data Structures · Notes',
            'Python · Programming',
            'C Language · Fundamentals',
            'Algorithms · Problem Solving',
            'PYQs · Previous Papers',
            'AI Assistant · Smart Help',
          ].map((item, i) => {
            const [a, b] = item.split(' · ')
            return (
              <span key={i} className="ticker__item">
                <em>{a}</em> <span className="ticker__sep">·</span> {b}
              </span>
            )
          })}
        </div>
      </div>

      {/* ── Semesters ─────────────────────────── */}
      <section style={{ borderTop: '1px solid var(--border)', padding: '80px 0' }}>
        <div className="reveal-scale">
          <span className="section-header-line" />
          <p
            style={{
              fontFamily: 'var(--font-mono)',
              fontSize: '12px',
              textTransform: 'uppercase',
              letterSpacing: '0.14em',
              color: 'var(--accent)',
            }}
          >
            Browse by Semester
          </p>
          <h2
            style={{
              fontFamily: 'var(--font-display)',
              fontSize: 'clamp(2rem, 4vw, 3rem)',
              lineHeight: 1.12,
              color: 'var(--fg)',
              marginTop: '16px',
              maxWidth: '20ch',
            }}
          >
            Select your semester to begin
          </h2>
        </div>

        <div
          style={{
            marginTop: '48px',
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))',
            gap: '20px',
          }}
        >
          {isLoading
            ? Array.from({ length: 4 }).map((_, i) => (
                <div
                  key={i}
                  style={{
                    height: '140px',
                    border: '1px solid var(--border)',
                    borderRadius: 'var(--radius)',
                    background: 'var(--surface)',
                    animation: 'pulse 2s infinite',
                  }}
                />
              ))
            : semesters?.map((semester, index) => (
                <Link
                  key={semester.id}
                  to={`/subjects?semester=${semester.id}`}
                  className="reveal-scale card-hover semester-card"
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
                  <p
                    style={{
                      fontFamily: 'var(--font-mono)',
                      fontSize: '11px',
                      textTransform: 'uppercase',
                      letterSpacing: '0.1em',
                      color: 'var(--accent-2)',
                    }}
                  >
                    {semester.subjects?.length || 0} Subjects
                  </p>
                  <h3
                    style={{
                      fontFamily: 'var(--font-display)',
                      fontSize: 'clamp(1.25rem, 2vw, 1.6rem)',
                      color: 'var(--fg)',
                      marginTop: '12px',
                    }}
                  >
                    Semester {semester.number}
                  </h3>
                  <div
                    className="semester-arrow"
                    style={{
                      marginTop: '16px',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '8px',
                      fontSize: '14px',
                      color: 'var(--muted)',
                    }}
                  >
                    <span>Explore</span>
                    <ArrowRight style={{ width: '16px', height: '16px' }} />
                  </div>
                </Link>
              ))}
        </div>
      </section>

      {/* ── Quick Access ──────────────────────── */}
      <section style={{ borderTop: '1px solid var(--border)', padding: '80px 0' }}>
        <div className="reveal-scale">
          <span className="section-header-line" />
          <p
            style={{
              fontFamily: 'var(--font-mono)',
              fontSize: '12px',
              textTransform: 'uppercase',
              letterSpacing: '0.14em',
              color: 'var(--accent)',
            }}
          >
            Quick Access
          </p>
          <h2
            style={{
              fontFamily: 'var(--font-display)',
              fontSize: 'clamp(2rem, 4vw, 3rem)',
              lineHeight: 1.12,
              color: 'var(--fg)',
              marginTop: '16px',
            }}
          >
            Jump right in
          </h2>
        </div>

        <div
          style={{
            marginTop: '48px',
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
            gap: '20px',
          }}
        >
          {[
            {
              to: '/subjects',
              icon: BookOpen,
              title: 'Browse Subjects',
              desc: 'Explore all subjects across semesters with detailed syllabi and resources.',
              color: 'var(--accent)',
            },
            {
              to: '/search',
              icon: TrendingUp,
              title: 'PYQ Analysis',
              desc: 'Analyze previous year questions and identify important topics.',
              color: 'var(--accent-2)',
            },
            {
              to: '/faculty',
              icon: GraduationCap,
              title: 'Faculty Resources',
              desc: 'Upload and manage academic resources for students.',
              color: 'var(--accent)',
            },
          ].map((card, i) => {
            const Icon = card.icon
            return (
              <Link
                key={card.to}
                to={card.to}
                className="reveal-scale card-hover quick-access-card"
                data-delay={(i + 1).toString()}
                style={{
                  display: 'block',
                  padding: 'clamp(24px, 3vw, 36px)',
                  border: '1px solid var(--border)',
                  borderRadius: 'var(--radius)',
                  textDecoration: 'none',
                  background: 'var(--bg)',
                }}
              >
                <Icon
                  className="quick-access-icon"
                  style={{ width: '24px', height: '24px', color: card.color }}
                />
                <h3
                  style={{
                    fontFamily: 'var(--font-display)',
                    fontSize: '20px',
                    color: 'var(--fg)',
                    marginTop: '16px',
                  }}
                >
                  {card.title}
                </h3>
                <p
                  style={{
                    fontSize: '14px',
                    color: 'var(--muted)',
                    marginTop: '8px',
                    lineHeight: 1.6,
                  }}
                >
                  {card.desc}
                </p>
              </Link>
            )
          })}
        </div>
      </section>

      {/* ── Stats ─────────────────────────────── */}
      <section style={{ borderTop: '1px solid var(--border)', padding: '80px 0' }}>
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))',
            gap: '20px',
          }}
        >
          {[
            { value: '39', label: 'Topics', sub: 'Across 2 subjects' },
            { value: '130', label: 'Resources', sub: 'Notes, videos, PYQs' },
            { value: '5', label: 'Units', sub: 'Per subject' },
            { value: '24/7', label: 'AI Help', sub: 'Always available' },
          ].map((stat, i) => (
            <AnimatedStat
              key={stat.label}
              target={stat.value}
              label={stat.label}
              sub={stat.sub}
              delay={i + 1}
            />
          ))}
        </div>
      </section>
    </div>
  )
}
