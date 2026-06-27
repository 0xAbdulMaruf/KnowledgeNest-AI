import { useState } from 'react'
import { GraduationCap, Send, CheckCircle } from 'lucide-react'
import { useSubjects, useSubjectUnits, useUnitTopics, useCreateResource } from '@/hooks/use-api'
import type { ResourceType } from '@/services/api'

const resourceTypes: { value: ResourceType; label: string }[] = [
  { value: 'college_notes', label: 'College Notes' },
  { value: 'external_notes', label: 'External Notes' },
  { value: 'pdf', label: 'PDF' },
  { value: 'video', label: 'Video' },
  { value: 'pyq', label: 'PYQ' },
  { value: 'important_questions', label: 'Important Questions' },
  { value: 'practice_questions', label: 'Practice Questions' },
  { value: 'coding_problems', label: 'Coding Problems' },
  { value: 'assignment', label: 'Assignment' },
  { value: 'book', label: 'Book' },
  { value: 'documentation', label: 'Documentation' },
]

export default function FacultyPage() {
  const [subjectId, setSubjectId] = useState<number | null>(null)
  const [unitId, setUnitId] = useState<number | null>(null)
  const [topicId, setTopicId] = useState<number | null>(null)
  const [type, setType] = useState<ResourceType>('college_notes')
  const [title, setTitle] = useState('')
  const [url, setUrl] = useState('')
  const [content, setContent] = useState('')
  const [success, setSuccess] = useState(false)

  const { data: subjects } = useSubjects()
  const { data: units } = useSubjectUnits(subjectId || 0)
  const { data: topics } = useUnitTopics(unitId || 0)
  const createMutation = useCreateResource()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!topicId || !title) return

    try {
      await createMutation.mutateAsync({
        topic_id: topicId,
        type,
        title,
        url: url || undefined,
        content: content || undefined,
      })
      setSuccess(true)
      setTitle('')
      setUrl('')
      setContent('')
      setTimeout(() => setSuccess(false), 3000)
    } catch {
      alert('Failed to create resource')
    }
  }

  return (
    <div className="space-y-0">
      {/* Header */}
      <section className="border-b border-[var(--border)] pb-12 pt-8">
        <p className="reveal font-[var(--font-mono)] text-xs uppercase tracking-[0.12em] text-[var(--accent)]" style={{ fontFamily: 'var(--font-mono)' }}>
          Faculty
        </p>
        <h1 className="reveal mt-4 font-[var(--font-display)] text-[clamp(2.5rem,5vw,4rem)] leading-[1.1] tracking-[-0.02em] text-[var(--fg)]" data-delay="1" style={{ fontFamily: 'var(--font-display)' }}>
          Resource Manager
        </h1>
        <p className="reveal mt-4 max-w-[54ch] text-[clamp(1rem,1.5vw,1.25rem)] leading-[1.7] text-[var(--muted)]" data-delay="2">
          Upload and manage academic resources for students
        </p>
      </section>

      {/* Form */}
      <section className="reveal border-t border-[var(--border)] py-[clamp(64px,10vh,140px)]" data-delay="3">
        <form onSubmit={handleSubmit} className="max-w-2xl space-y-8">
          {/* Cascading Selects */}
          <div className="grid grid-cols-1 gap-0 sm:grid-cols-3">
            <div className="border border-[var(--border)] p-4">
              <label className="mb-2 block font-[var(--font-mono)] text-[0.6875rem] uppercase tracking-[0.1em] text-[var(--muted)]" style={{ fontFamily: 'var(--font-mono)' }}>
                Subject
              </label>
              <select
                value={subjectId || ''}
                onChange={(e) => {
                  setSubjectId(Number(e.target.value) || null)
                  setUnitId(null)
                  setTopicId(null)
                }}
                className="w-full border border-[var(--border)] bg-[var(--bg)] px-3 py-2 text-sm text-[var(--fg)] outline-none transition-colors focus:border-[var(--accent)]"
              >
                <option value="">Select subject</option>
                {subjects?.map((s) => (
                  <option key={s.id} value={s.id}>{s.name}</option>
                ))}
              </select>
            </div>

            <div className="border border-[var(--border)] p-4">
              <label className="mb-2 block font-[var(--font-mono)] text-[0.6875rem] uppercase tracking-[0.1em] text-[var(--muted)]" style={{ fontFamily: 'var(--font-mono)' }}>
                Unit
              </label>
              <select
                value={unitId || ''}
                onChange={(e) => {
                  setUnitId(Number(e.target.value) || null)
                  setTopicId(null)
                }}
                disabled={!subjectId}
                className="w-full border border-[var(--border)] bg-[var(--bg)] px-3 py-2 text-sm text-[var(--fg)] outline-none transition-colors focus:border-[var(--accent)] disabled:opacity-40"
              >
                <option value="">Select unit</option>
                {units?.map((u) => (
                  <option key={u.id} value={u.id}>{u.name}</option>
                ))}
              </select>
            </div>

            <div className="border border-[var(--border)] p-4">
              <label className="mb-2 block font-[var(--font-mono)] text-[0.6875rem] uppercase tracking-[0.1em] text-[var(--muted)]" style={{ fontFamily: 'var(--font-mono)' }}>
                Topic
              </label>
              <select
                value={topicId || ''}
                onChange={(e) => setTopicId(Number(e.target.value) || null)}
                disabled={!unitId}
                className="w-full border border-[var(--border)] bg-[var(--bg)] px-3 py-2 text-sm text-[var(--fg)] outline-none transition-colors focus:border-[var(--accent)] disabled:opacity-40"
              >
                <option value="">Select topic</option>
                {topics?.map((t) => (
                  <option key={t.id} value={t.id}>{t.name}</option>
                ))}
              </select>
            </div>
          </div>

          {/* Resource Type */}
          <div>
            <label className="mb-3 block font-[var(--font-mono)] text-[0.6875rem] uppercase tracking-[0.1em] text-[var(--muted)]" style={{ fontFamily: 'var(--font-mono)' }}>
              Resource Type
            </label>
            <div className="flex flex-wrap gap-0">
              {resourceTypes.map((rt) => (
                <button
                  key={rt.value}
                  type="button"
                  onClick={() => setType(rt.value)}
                  className={`border px-4 py-2 text-sm transition-all ${
                    type === rt.value
                      ? 'border-[var(--accent)] bg-[var(--accent)] text-[var(--bg)]'
                      : 'border-[var(--border)] text-[var(--muted)] hover:border-[var(--muted)] hover:text-[var(--fg)]'
                  }`}
                >
                  {rt.label}
                </button>
              ))}
            </div>
          </div>

          {/* Title */}
          <div>
            <label className="mb-2 block font-[var(--font-mono)] text-[0.6875rem] uppercase tracking-[0.1em] text-[var(--muted)]" style={{ fontFamily: 'var(--font-mono)' }}>
              Title *
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Resource title"
              required
              className="w-full border border-[var(--border)] bg-[var(--bg)] px-4 py-3 text-[var(--fg)] placeholder-[var(--muted)] outline-none transition-colors focus:border-[var(--accent)]"
            />
          </div>

          {/* URL */}
          <div>
            <label className="mb-2 block font-[var(--font-mono)] text-[0.6875rem] uppercase tracking-[0.1em] text-[var(--muted)]" style={{ fontFamily: 'var(--font-mono)' }}>
              URL
            </label>
            <input
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://..."
              className="w-full border border-[var(--border)] bg-[var(--bg)] px-4 py-3 text-[var(--fg)] placeholder-[var(--muted)] outline-none transition-colors focus:border-[var(--accent)]"
            />
          </div>

          {/* Content */}
          <div>
            <label className="mb-2 block font-[var(--font-mono)] text-[0.6875rem] uppercase tracking-[0.1em] text-[var(--muted)]" style={{ fontFamily: 'var(--font-mono)' }}>
              Content
            </label>
            <textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder="Resource content or description..."
              rows={4}
              className="w-full border border-[var(--border)] bg-[var(--bg)] px-4 py-3 text-[var(--fg)] placeholder-[var(--muted)] outline-none transition-colors focus:border-[var(--accent)]"
            />
          </div>

          {/* Submit */}
          <div className="flex items-center gap-4">
            <button
              type="submit"
              disabled={createMutation.isPending || !topicId || !title}
              className="flex items-center gap-2 bg-[var(--accent)] px-6 py-3 text-sm font-semibold text-[var(--bg)] transition-opacity hover:opacity-90 disabled:opacity-40"
            >
              <Send className="h-4 w-4" />
              {createMutation.isPending ? 'Submitting...' : 'Submit Resource'}
            </button>
            {success && (
              <div className="flex items-center gap-2 text-[var(--accent)]">
                <CheckCircle className="h-4 w-4" />
                <span className="font-[var(--font-mono)] text-sm" style={{ fontFamily: 'var(--font-mono)' }}>Resource added successfully!</span>
              </div>
            )}
          </div>
        </form>
      </section>
    </div>
  )
}
