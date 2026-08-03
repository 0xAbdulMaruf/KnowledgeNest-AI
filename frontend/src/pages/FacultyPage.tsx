import axios from 'axios'
import { useEffect, useMemo, useRef, useState } from 'react'
import { CheckCircle, Clock3, Edit3, Filter, Lock, LogOut, Send, Trash2, X } from 'lucide-react'
import { useSubjects, useSubjectUnits, useUnitTopics, useCreateResource, useDeleteResource, useFacultyActivities, useFacultyResources, useFacultyUnlock, useRestoreResource, useUpdateResource } from '@/hooks/use-api'
import { setFacultySessionToken } from '@/services/api'
import type { Resource, ResourceType } from '@/services/api'

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
  { value: 'image', label: 'Image' },
]

export default function FacultyPage() {
  const [loginName, setLoginName] = useState('')
  const [password, setPassword] = useState('')
  const [facultyToken, setFacultyTokenState] = useState<string | null>(() => sessionStorage.getItem('faculty_session_token'))
  const [subjectId, setSubjectId] = useState<number | null>(null)
  const [unitId, setUnitId] = useState<number | null>(null)
  const [topicId, setTopicId] = useState<number | null>(null)
  const [type, setType] = useState<ResourceType>('college_notes')
  const [title, setTitle] = useState('')
  const [url, setUrl] = useState('')
  const [content, setContent] = useState('')
  const [editingResourceId, setEditingResourceId] = useState<number | null>(null)
  const [saveMode, setSaveMode] = useState<'create' | 'update' | null>(null)
  const [success, setSuccess] = useState(false)
  const [submitError, setSubmitError] = useState('')
  const [unlockError, setUnlockError] = useState('')
  const [deleteTarget, setDeleteTarget] = useState<number | null>(null)
  const [typeFilter, setTypeFilter] = useState<ResourceType | null>(null)
  const [formDirty, setFormDirty] = useState(false)
  const formRef = useRef<HTMLFormElement>(null)

  // Decode logged-in teacher name from session token
  const teacherName = useMemo(() => {
    if (!facultyToken) return ''
    try {
      const base64url = facultyToken.replace(/-/g, '+').replace(/_/g, '/')
      const decoded = atob(base64url)
      const payloadStr = decoded.split('.')[0]
      const payload = JSON.parse(atob(payloadStr.replace(/-/g, '+').replace(/_/g, '/')))
      return payload.teacher_name || ''
    } catch {
      return ''
    }
  }, [facultyToken])

  const { data: subjects } = useSubjects()
  const { data: units } = useSubjectUnits(subjectId || 0)
  const { data: topics } = useUnitTopics(unitId || 0)
  const unlocked = Boolean(facultyToken)
  const { data: facultyResources } = useFacultyResources(unlocked && !!topicId, topicId || undefined)
  const { data: activityItems } = useFacultyActivities(unlocked)
  const unlockMutation = useFacultyUnlock()
  const createMutation = useCreateResource()
  const updateMutation = useUpdateResource()
  const deleteMutation = useDeleteResource()
  const restoreMutation = useRestoreResource()

  useEffect(() => {
    if (facultyToken) {
      setFacultySessionToken(facultyToken)
    }
  }, [facultyToken])

  const orderedResources = useMemo(
    () => [...(facultyResources || [])].sort((left, right) => right.id - left.id),
    [facultyResources]
  )

  const filteredResources = useMemo(
    () => typeFilter ? orderedResources.filter((r) => r.type === typeFilter) : orderedResources,
    [orderedResources, typeFilter]
  )

  // Count resources by type
  const typeCounts = useMemo(() => {
    const counts: Record<string, number> = {}
    for (const r of facultyResources || []) {
      if (!r.deleted_at) counts[r.type] = (counts[r.type] || 0) + 1
    }
    return counts
  }, [facultyResources])

  const recentActivities = useMemo(
    () => [...(activityItems || [])].sort((left, right) => right.id - left.id).slice(0, 10),
    [activityItems]
  )

  const handleLogout = () => {
    setFacultySessionToken(null)
    setFacultyTokenState(null)
    setSubjectId(null)
    setUnitId(null)
    setTopicId(null)
    resetResourceForm()
  }

  const handleUnlock = async (e: React.FormEvent) => {
    e.preventDefault()
    setUnlockError('')
    try {
      const response = await unlockMutation.mutateAsync({ teacher_name: loginName, password })
      setFacultyTokenState(response.access_token)
    } catch {
      setUnlockError('Invalid teacher name or password')
    }
  }

  const handleDelete = async (resourceId: number) => {
    if (!window.confirm('Delete this resource? This will hide it from students.')) return
    try {
      setDeleteTarget(resourceId)
      await deleteMutation.mutateAsync(resourceId)
    } finally {
      setDeleteTarget(null)
    }
  }

  const handleRestore = async (resource: Resource) => {
    try {
      await restoreMutation.mutateAsync(resource.id)
      handleEdit(resource)
    } catch (error) {
      let message = 'Failed to restore resource'
      if (axios.isAxiosError(error)) {
        const detail = error.response?.data?.detail
        const status = error.response?.status
        if (typeof detail === 'string' && detail.trim()) {
          message = `${message}: ${detail}`
        } else if (status) {
          message = `${message}: HTTP ${status}`
        }
      }
      setSubmitError(message)
      alert(message)
    }
  }

  const resetResourceForm = () => {
    setEditingResourceId(null)
    setType('college_notes')
    setTitle('')
    setUrl('')
    setContent('')
    setSaveMode(null)
    setFormDirty(false)
  }

  const confirmDiscard = (action: () => void) => {
    if (formDirty && !window.confirm('You have unsaved changes. Discard them?')) return
    action()
  }

  const handleEdit = (resource: Resource) => {
    // Clicking the same resource being edited — just scroll to form, no confirm needed
    if (resource.id === editingResourceId) {
      setTimeout(() => {
        formRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }, 50)
      return
    }
    const switchResource = () => {
      setEditingResourceId(resource.id)
      setType(resource.type)
      setTitle(resource.title)
      setUrl(resource.url || '')
      setContent(resource.content || '')
      setSaveMode(null)
      setSuccess(false)
      setSubmitError('')
      setFormDirty(false)
      setTimeout(() => {
        formRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }, 50)
    }
    confirmDiscard(switchResource)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!topicId || !title) return

    try {
      setSubmitError('')
      const wasEditing = Boolean(editingResourceId)
      if (editingResourceId) {
        await updateMutation.mutateAsync({
          resourceId: editingResourceId,
          payload: {
            topic_id: topicId,
            type,
            title,
            url,
            content,
          },
        })
      } else {
        await createMutation.mutateAsync({
          topic_id: topicId,
          type,
          title,
          url,
          content,
        })
      }
      setSuccess(true)
      resetResourceForm()
      setFormDirty(false)
      setSaveMode(wasEditing ? 'update' : 'create')
      setTimeout(() => setSuccess(false), 3000)
    } catch (error) {
      let message = editingResourceId ? 'Failed to update resource' : 'Failed to create resource'
      if (axios.isAxiosError(error)) {
        const detail = error.response?.data?.detail
        const status = error.response?.status
        if (typeof detail === 'string' && detail.trim()) {
          message = `${message}: ${detail}`
        } else if (status) {
          message = `${message}: HTTP ${status}`
        }
      }
      setSubmitError(message)
      alert(message)
    }
  }

  if (!unlocked) {
    return (
      <div className="space-y-0">
        <section className="border-b border-[var(--border)] pb-12 pt-8">
          <p className="reveal font-[var(--font-mono)] text-xs uppercase tracking-[0.12em] text-[var(--accent)]" style={{ fontFamily: 'var(--font-mono)' }}>
            Faculty
          </p>
          <h1 className="reveal mt-4 font-[var(--font-display)] text-[clamp(2.5rem,5vw,4rem)] leading-[1.1] tracking-[-0.02em] text-[var(--fg)]" data-delay="1" style={{ fontFamily: 'var(--font-display)' }}>
            Teacher Access Required
          </h1>
          <p className="reveal mt-4 max-w-[54ch] text-[clamp(1rem,1.5vw,1.25rem)] leading-[1.7] text-[var(--muted)]" data-delay="2">
            Unlock the faculty resource manager with your teacher name and password.
          </p>
        </section>

        <section className="reveal border-t border-[var(--border)] py-[clamp(64px,10vh,140px)]" data-delay="3">
          <form onSubmit={handleUnlock} className="max-w-xl space-y-6 border border-[var(--border)] p-6">
            <div>
              <label className="mb-2 block font-[var(--font-mono)] text-[0.6875rem] uppercase tracking-[0.1em] text-[var(--muted)]" style={{ fontFamily: 'var(--font-mono)' }}>
                Teacher Name
              </label>
              <input
                value={loginName}
                onChange={(event) => setLoginName(event.target.value)}
                className="w-full border border-[var(--border)] bg-[var(--bg)] px-4 py-3 text-[var(--fg)] outline-none focus:border-[var(--accent)]"
                placeholder="Enter teacher name"
              />
            </div>
            <div>
              <label className="mb-2 block font-[var(--font-mono)] text-[0.6875rem] uppercase tracking-[0.1em] text-[var(--muted)]" style={{ fontFamily: 'var(--font-mono)' }}>
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                className="w-full border border-[var(--border)] bg-[var(--bg)] px-4 py-3 text-[var(--fg)] outline-none focus:border-[var(--accent)]"
                placeholder="Teacher password"
              />
            </div>
            {unlockError && <p className="text-sm text-red-500">{unlockError}</p>}
            <button
              type="submit"
              disabled={unlockMutation.isPending || !loginName || !password}
              className="flex items-center gap-2 bg-[var(--accent)] px-6 py-3 text-sm font-semibold text-[var(--bg)] transition-opacity hover:opacity-90 disabled:opacity-40"
            >
              <Lock className="h-4 w-4" />
              {unlockMutation.isPending ? 'Unlocking...' : 'Unlock Faculty Page'}
            </button>
          </form>
        </section>
      </div>
    )
  }

  return (
    <div className="space-y-0">
      {/* Header */}
      <section className="border-b border-[var(--border)] pb-12 pt-8">
        <div className="flex items-center justify-between gap-4">
          <div>
            <p className="reveal font-[var(--font-mono)] text-xs uppercase tracking-[0.12em] text-[var(--accent)]" style={{ fontFamily: 'var(--font-mono)' }}>
              Faculty
            </p>
            <h1 className="reveal mt-4 font-[var(--font-display)] text-[clamp(2.5rem,5vw,4rem)] leading-[1.1] tracking-[-0.02em] text-[var(--fg)]" data-delay="1" style={{ fontFamily: 'var(--font-display)' }}>
              Resource Manager
            </h1>
            <p className="reveal mt-4 max-w-[54ch] text-[clamp(1rem,1.5vw,1.25rem)] leading-[1.7] text-[var(--muted)]" data-delay="2">
              Upload and manage academic resources for students
            </p>
          </div>
          {teacherName && (
            <div className="reveal flex items-center gap-3" data-delay="3">
              <span className="font-[var(--font-mono)] text-xs uppercase tracking-[0.06em] text-[var(--muted)]" style={{ fontFamily: 'var(--font-mono)' }}>
                {teacherName}
              </span>
              <button
                type="button"
                onClick={handleLogout}
                className="flex items-center gap-1.5 border border-[var(--border)] px-3 py-2 text-xs text-[var(--muted)] transition-colors hover:border-red-500 hover:text-red-500"
                title="Logout"
              >
                <LogOut className="h-3.5 w-3.5" />
                Logout
              </button>
            </div>
          )}
        </div>
      </section>

      <section className="reveal border-t border-[var(--border)] py-[clamp(48px,8vh,96px)]" data-delay="2">
        <div className="grid gap-8 lg:grid-cols-[2fr_1fr]">
          {/* Left: Form + Current Resources */}
          <div className="space-y-8">
            {/* New Resource Form */}
            <form ref={formRef} key={editingResourceId ?? 'new'} onSubmit={handleSubmit} onKeyDown={(e) => { if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') handleSubmit(e) }} className="space-y-8 border border-[var(--border)] p-6">
          <div className="flex items-center justify-between gap-4 border-b border-[var(--border)] pb-4">
            <div>
              <p className="font-[var(--font-mono)] text-[0.6875rem] uppercase tracking-[0.1em] text-[var(--muted)]" style={{ fontFamily: 'var(--font-mono)' }}>
                {editingResourceId ? 'Edit Resource' : 'New Resource'}
              </p>
              <h3 className="mt-1 text-lg text-[var(--fg)]">
                {editingResourceId ? 'Update the selected resource' : 'Create a new resource for the selected topic'}
              </h3>
            </div>
            {editingResourceId && (
              <button
                type="button"
                onClick={() => confirmDiscard(resetResourceForm)}
                className="flex items-center gap-2 border border-[var(--border)] px-3 py-2 text-xs text-[var(--muted)] transition-colors hover:border-[var(--fg)] hover:text-[var(--fg)]"
              >
                <X className="h-3.5 w-3.5" />
                Cancel edit
              </button>
            )}
          </div>

          {/* Cascading Selects */}
          <div className="grid grid-cols-1 gap-0 sm:grid-cols-3">
            <div className="border border-[var(--border)] p-4">
              <label className="mb-2 block font-[var(--font-mono)] text-[0.6875rem] uppercase tracking-[0.1em] text-[var(--muted)]" style={{ fontFamily: 'var(--font-mono)' }}>
                Subject
              </label>
              <select
                value={subjectId || ''}
                onChange={(e) => {
                  confirmDiscard(() => {
                    setSubjectId(Number(e.target.value) || null)
                    setUnitId(null)
                    setTopicId(null)
                    setSuccess(false)
                    resetResourceForm()
                  })
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
                  confirmDiscard(() => {
                    setUnitId(Number(e.target.value) || null)
                    setTopicId(null)
                    setSuccess(false)
                    resetResourceForm()
                  })
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
                onChange={(e) => {
                  confirmDiscard(() => {
                    setTopicId(Number(e.target.value) || null)
                    setSuccess(false)
                    resetResourceForm()
                  })
                }}
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
                <span
                  key={rt.value}
                  aria-disabled="true"
                  className={`border px-4 py-2 text-sm ${
                    type === rt.value
                      ? 'border-[var(--accent)] bg-[var(--accent)] text-[var(--bg)]'
                      : 'border-[var(--border)] text-[var(--muted)]'
                  }`}
                >
                  {rt.label}
                </span>
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
              onChange={(e) => { setTitle(e.target.value); setFormDirty(true) }}
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
              onChange={(e) => { setUrl(e.target.value); setFormDirty(true) }}
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
              onChange={(e) => { setContent(e.target.value); setFormDirty(true) }}
              placeholder="Resource content or description..."
              rows={4}
              className="w-full border border-[var(--border)] bg-[var(--bg)] px-4 py-3 text-[var(--fg)] placeholder-[var(--muted)] outline-none transition-colors focus:border-[var(--accent)]"
            />
          </div>

          {/* Submit */}
          <div className="flex items-center gap-4">
            <button
              type="submit"
              disabled={(createMutation.isPending || updateMutation.isPending) || !topicId || !title}
              title={editingResourceId ? 'Update (Ctrl+Enter)' : 'Submit (Ctrl+Enter)'}
              className="flex items-center gap-2 bg-[var(--accent)] px-6 py-3 text-sm font-semibold text-[var(--bg)] transition-opacity hover:opacity-90 disabled:opacity-40"
            >
              <Send className="h-4 w-4" />
              {editingResourceId ? (updateMutation.isPending ? 'Updating...' : 'Update Resource') : (createMutation.isPending ? 'Submitting...' : 'Submit Resource')}
            </button>
            {success && (
              <div className="flex items-center gap-2 text-[var(--accent)]">
                <CheckCircle className="h-4 w-4" />
                <span className="font-[var(--font-mono)] text-sm" style={{ fontFamily: 'var(--font-mono)' }}>{saveMode === 'update' ? 'Resource updated successfully!' : 'Resource added successfully!'}</span>
              </div>
            )}
          </div>

          {submitError && (
            <p className="border border-red-500/40 bg-red-500/10 px-4 py-3 text-sm text-red-500">
              {submitError}
            </p>
          )}
        </form>

        {/* Current Resources */}
        <div className="space-y-4 border border-[var(--border)] p-6">
          <div className="flex items-center justify-between gap-4">
            <h2 className="font-[var(--font-display)] text-2xl text-[var(--fg)]" style={{ fontFamily: 'var(--font-display)' }}>
              {topicId ? 'Current Resources' : 'Select a Topic'}
            </h2>
            <span className="font-[var(--font-mono)] text-xs uppercase tracking-[0.1em] text-[var(--muted)]" style={{ fontFamily: 'var(--font-mono)' }}>
              {filteredResources.length}{typeFilter ? '' : `/${orderedResources.length}`} items
            </span>
          </div>

          {/* Type count breakdown */}
          {topicId && orderedResources.length > 0 && (
            <p className="text-xs text-[var(--muted)]">
              {Object.entries(typeCounts).map(([t, count], i, arr) => {
                const label = resourceTypes.find((rt) => rt.value === t)?.label || t
                return (
                  <span key={t}>
                    <span className="font-medium text-[var(--fg)]">{count}</span> {label}
                    {i < arr.length - 1 ? ' · ' : ''}
                  </span>
                )
              })}
            </p>
          )}

          {/* Type filter chips */}
          {topicId && orderedResources.length > 0 && (
            <div className="flex flex-wrap items-center gap-2 border-b border-[var(--border)] pb-3">
              <Filter className="h-3.5 w-3.5 text-[var(--muted)]" />
              <button
                type="button"
                onClick={() => setTypeFilter(null)}
                className={`px-3 py-1 text-xs transition-all ${
                  !typeFilter
                    ? 'bg-[var(--accent)] text-[var(--bg)]'
                    : 'border border-[var(--border)] text-[var(--muted)] hover:border-[var(--muted)]'
                }`}
              >
                All ({orderedResources.length})
              </button>
              {resourceTypes.filter((rt) => typeCounts[rt.value]).slice(0, 5).map((rt) => (
                <button
                  key={rt.value}
                  type="button"
                  onClick={() => setTypeFilter(typeFilter === rt.value ? null : rt.value)}
                  className={`px-3 py-1 text-xs transition-all ${
                    typeFilter === rt.value
                      ? 'bg-[var(--accent)] text-[var(--bg)]'
                      : 'border border-[var(--border)] text-[var(--muted)] hover:border-[var(--muted)]'
                  }`}
                >
                  {rt.label} ({typeCounts[rt.value]})
                </button>
              ))}
            </div>
          )}

          {topicId ? filteredResources.length > 0 ? (
            <div className="space-y-3">
              {filteredResources.map((resource) => (
                <div
                  key={resource.id}
                  className={`flex items-center justify-between gap-4 border px-4 py-3 transition-colors ${
                    resource.id === editingResourceId
                      ? 'border-[var(--accent)] bg-[var(--accent)]/5'
                      : resource.deleted_at
                        ? 'border-dashed border-red-500/40 bg-red-500/5'
                        : 'border-[var(--border)]'
                  }`}
                >
                  <div className="min-w-0">
                    <p className="truncate text-sm text-[var(--fg)]">{resource.title}</p>
                    <p className="mt-1 text-xs text-[var(--muted)]">{resource.type.replace(/_/g, ' ')}</p>
                    {resource.deleted_at && (
                      <p className="mt-1 text-xs text-red-500">
                        Deleted{resource.deleted_by ? ` by ${resource.deleted_by}` : ''}
                      </p>
                    )}
                  </div>
                  <div className="flex items-center gap-2">
                    {resource.deleted_at ? (
                      <button
                        type="button"
                        onClick={() => handleRestore(resource)}
                        disabled={restoreMutation.isPending}
                        className="flex items-center gap-2 border border-[var(--border)] px-3 py-2 text-xs text-[var(--accent)] transition-colors hover:border-[var(--accent)] disabled:opacity-40"
                      >
                        <X className="h-3.5 w-3.5 rotate-45" />
                        {restoreMutation.isPending ? 'Restoring...' : 'Restore & Edit'}
                      </button>
                    ) : (
                      <>
                        <button
                          type="button"
                          onClick={() => handleEdit(resource)}
                          className="flex items-center gap-2 border border-[var(--border)] px-3 py-2 text-xs text-[var(--muted)] transition-colors hover:border-[var(--accent)] hover:text-[var(--accent)]"
                        >
                          <Edit3 className="h-3.5 w-3.5" />
                          Edit
                        </button>
                        <button
                          type="button"
                          onClick={() => handleDelete(resource.id)}
                          disabled={deleteMutation.isPending && deleteTarget === resource.id}
                          className="flex items-center gap-2 border border-[var(--border)] px-3 py-2 text-xs text-[var(--muted)] transition-colors hover:border-red-500 hover:text-red-500 disabled:opacity-40"
                        >
                          <Trash2 className="h-3.5 w-3.5" />
                          {deleteMutation.isPending && deleteTarget === resource.id ? 'Deleting...' : 'Delete'}
                        </button>
                      </>
                    )}
                  </div>
                </div>
              ))}
            </div>
          ) : typeFilter ? (
            <div className="flex flex-col items-center gap-3 py-8 text-center">
              <Filter className="h-8 w-8 text-[var(--muted)] opacity-30" />
              <p className="text-sm text-[var(--muted)]">No resources match this filter</p>
              <button type="button" onClick={() => setTypeFilter(null)} className="text-xs text-[var(--accent)] hover:underline">
                Clear filter
              </button>
            </div>
          ) : (
            <div className="flex flex-col items-center gap-3 py-8 text-center">
              <Send className="h-8 w-8 text-[var(--muted)] opacity-30" />
              <p className="text-sm text-[var(--muted)]">No resources have been added for this topic yet.</p>
              <p className="text-xs text-[var(--muted)]">Use the form above to add your first resource.</p>
            </div>
          ) : (
            <div className="flex flex-col items-center gap-3 py-8 text-center">
              <Edit3 className="h-8 w-8 text-[var(--muted)] opacity-30" />
              <p className="text-sm text-[var(--muted)]">Select a subject, unit, and topic to load resources</p>
            </div>
          )}
        </div>
      </div>

      {/* Right: Recent Activity */}
      <div className="space-y-4 border border-[var(--border)] p-6">
        <div className="flex items-center gap-2">
          <Clock3 className="h-4 w-4 text-[var(--accent)]" />
          <h2 className="font-[var(--font-display)] text-2xl text-[var(--fg)]" style={{ fontFamily: 'var(--font-display)' }}>
            Recent Activity
          </h2>
        </div>
        {recentActivities.length > 0 ? (
          <div className="space-y-3">
            {recentActivities.map((activity) => (
              <div key={activity.id} className="border border-[var(--border)] px-4 py-3 text-sm text-[var(--fg)]">
                <p className="font-medium">{activity.teacher_name} {activity.action} resource #{activity.resource_id}</p>
                <p className="mt-1 text-xs text-[var(--muted)]">{new Date(activity.created_at).toLocaleString()}</p>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-sm text-[var(--muted)]">Activity will appear here after create or delete actions.</p>
        )}
      </div>
    </div>
  </section>
    </div>
  )
}
