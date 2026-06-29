import axios from 'axios'
import { useEffect, useMemo, useState } from 'react'
import { CheckCircle, Clock3, Edit3, Lock, Send, Trash2, X } from 'lucide-react'
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
  const [teacherName, setTeacherName] = useState('')
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

  const recentActivities = useMemo(
    () => [...(activityItems || [])].sort((left, right) => right.id - left.id).slice(0, 10),
    [activityItems]
  )

  const handleUnlock = async (e: React.FormEvent) => {
    e.preventDefault()
    setUnlockError('')
    try {
      const response = await unlockMutation.mutateAsync({ teacher_name: teacherName, password })
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
  }

  const handleEdit = (resource: Resource) => {
    setEditingResourceId(resource.id)
    setType(resource.type)
    setTitle(resource.title)
    setUrl(resource.url || '')
    setContent(resource.content || '')
    setSaveMode(null)
    setSuccess(false)
    setSubmitError('')
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
                value={teacherName}
                onChange={(event) => setTeacherName(event.target.value)}
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
              disabled={unlockMutation.isPending || !teacherName || !password}
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

      <section className="reveal border-t border-[var(--border)] py-[clamp(48px,8vh,96px)]" data-delay="2">
        <div className="grid gap-8 lg:grid-cols-[1.5fr_1fr]">
          <div className="space-y-4 border border-[var(--border)] p-6">
            <div className="flex items-center justify-between gap-4">
              <h2 className="font-[var(--font-display)] text-2xl text-[var(--fg)]" style={{ fontFamily: 'var(--font-display)' }}>
                {topicId ? 'Current Resources' : 'Select a Topic'}
              </h2>
              <span className="font-[var(--font-mono)] text-xs uppercase tracking-[0.1em] text-[var(--muted)]" style={{ fontFamily: 'var(--font-mono)' }}>
                {orderedResources.length} items
              </span>
            </div>
            {topicId ? orderedResources.length > 0 ? (
              <div className="space-y-3">
                {orderedResources.map((resource) => (
                  <div
                    key={resource.id}
                    className={`flex items-center justify-between gap-4 border px-4 py-3 ${resource.deleted_at ? 'border-dashed border-red-500/40 bg-red-500/5' : 'border-[var(--border)]'}`}
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
            ) : (
              <p className="text-sm text-[var(--muted)]">No resources have been added for this topic yet.</p>
            ) : (
              <p className="text-sm text-[var(--muted)]">Select a subject, unit, and topic to load the current resources for editing.</p>
            )}
          </div>

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

      {/* Form */}
      <section className="reveal border-t border-[var(--border)] py-[clamp(64px,10vh,140px)]" data-delay="3">
        <form onSubmit={handleSubmit} className="max-w-2xl space-y-8">
          <div className="flex items-center justify-between gap-4 border border-[var(--border)] px-4 py-3">
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
                onClick={resetResourceForm}
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
                  setSubjectId(Number(e.target.value) || null)
                  setUnitId(null)
                  setTopicId(null)
                  setSuccess(false)
                  resetResourceForm()
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
                  setSuccess(false)
                  resetResourceForm()
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
                  setTopicId(Number(e.target.value) || null)
                  setSuccess(false)
                  resetResourceForm()
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
              disabled={(createMutation.isPending || updateMutation.isPending) || !topicId || !title}
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
            <p className="max-w-2xl border border-red-500/40 bg-red-500/10 px-4 py-3 text-sm text-red-500">
              {submitError}
            </p>
          )}
        </form>
      </section>
    </div>
  )
}
