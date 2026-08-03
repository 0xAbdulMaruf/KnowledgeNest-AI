import { useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { ChevronRight, BookOpen, FileText, Video, HelpCircle, Code, ExternalLink } from 'lucide-react'
import { useTopic, useTopicResources, useRecommendations } from '@/hooks/use-api'
import RecommendedTopics from '@/components/recommendation/RecommendedTopics'
import ResourceTypeIcon from '@/components/resource/ResourceTypeIcon'
import type { Resource, ResourceType } from '@/services/api'

const resourceTabs: { value: ResourceType | 'all'; label: string; icon: typeof BookOpen }[] = [
  { value: 'all', label: 'All', icon: BookOpen },
  { value: 'college_notes', label: 'Notes', icon: FileText },
  { value: 'external_notes', label: 'External', icon: ExternalLink },
  { value: 'video', label: 'Videos', icon: Video },
  { value: 'pyq', label: 'PYQs', icon: HelpCircle },
  { value: 'coding_problems', label: 'Code', icon: Code },
]

export default function TopicPage() {
  const { id } = useParams<{ id: string }>()
  const topicId = Number(id)
  const { data: topic, isLoading } = useTopic(topicId)
  const { data: resources } = useTopicResources(topicId)
  const [activeTab, setActiveTab] = useState<ResourceType | 'all'>('all')

  if (isLoading) {
    return (
      <div className="space-y-8">
        <div className="h-4 w-48 animate-pulse bg-[var(--surface)]" />
        <div className="h-8 w-64 animate-pulse bg-[var(--surface)]" />
        <div className="h-64 animate-pulse border border-[var(--border)] bg-[var(--surface)]" />
      </div>
    )
  }

  if (!topic) {
    return (
      <div className="flex flex-col items-center justify-center py-24">
        <p className="text-[var(--muted)]">Topic not found.</p>
        <Link to="/subjects" className="mt-4 text-[var(--accent)] hover:underline">
          Back to subjects
        </Link>
      </div>
    )
  }

  // Group resources by type
  const resourcesByType: Record<string, Resource[]> = {}
  if (resources) {
    resources.forEach((r: Resource) => {
      if (!resourcesByType[r.type]) {
        resourcesByType[r.type] = []
      }
      resourcesByType[r.type].push(r)
    })
  }

  // Filter resources by active tab
  const filteredResources = activeTab === 'all'
    ? (resources || [])
    : (resourcesByType[activeTab] || [])

  return (
    <div>
      {/* Breadcrumb */}
      <nav className="reveal flex items-center gap-2 font-[var(--font-mono)] text-xs uppercase tracking-[0.06em]" style={{ fontFamily: 'var(--font-mono)' }}>
        <Link to="/subjects" className="text-[var(--muted)] transition-colors hover:text-[var(--fg)]">
          Subjects
        </Link>
        {topic.subject_name && (
          <>
            <ChevronRight className="h-3 w-3 text-[var(--muted)]" />
            <Link to={`/subjects/${topic.subject_id}`} className="text-[var(--muted)] transition-colors hover:text-[var(--fg)]">
              {topic.subject_name}
            </Link>
          </>
        )}
        {topic.unit_name && (
          <>
            <ChevronRight className="h-3 w-3 text-[var(--muted)]" />
            <span className="text-[var(--muted)]">{topic.unit_name}</span>
          </>
        )}
        <ChevronRight className="h-3 w-3 text-[var(--muted)]" />
        <span className="text-[var(--fg)]">{topic.name}</span>
      </nav>

      {/* Topic Header */}
      <div className="reveal mt-8 border border-[var(--border)] p-[clamp(24px,3vw,40px)]" data-delay="1">
        <p className="font-[var(--font-mono)] text-[0.6875rem] uppercase tracking-[0.1em] text-[var(--accent-2)]" style={{ fontFamily: 'var(--font-mono)' }}>
          {topic.subject_name || 'Subject'} · {topic.unit_name || 'Unit'}
        </p>
        <h1 className="mt-4 font-[var(--font-display)] text-[clamp(2rem,4vw,3.5rem)] leading-[1.12] tracking-[-0.015em] text-[var(--fg)]" style={{ fontFamily: 'var(--font-display)' }}>
          {topic.name}
        </h1>
        {topic.description && (
          <p className="mt-6 max-w-[680px] text-[clamp(1rem,1.3vw,1.125rem)] leading-[1.8] text-[var(--muted)]">
            {topic.description}
          </p>
        )}
        {topic.tags && topic.tags.length > 0 && (
          <div className="mt-6 flex flex-wrap gap-2">
            {topic.tags.map((tag: string) => (
              <span key={tag} className="badge-editorial">
                {tag}
              </span>
            ))}
          </div>
        )}
        {topic.importance_score !== undefined && (
          <div className="mt-6 flex items-center gap-3">
            <span className="font-[var(--font-mono)] text-xs uppercase tracking-[0.06em] text-[var(--muted)]" style={{ fontFamily: 'var(--font-mono)' }}>
              Importance
            </span>
            <div className="h-1.5 w-32 bg-[var(--border)]">
              <div
                className="h-full bg-[var(--accent)]"
                style={{ width: `${(topic.importance_score || 0) * 100}%` }}
              />
            </div>
            <span className="font-[var(--font-mono)] text-xs text-[var(--accent)]" style={{ fontFamily: 'var(--font-mono)' }}>
              {Math.round((topic.importance_score || 0) * 100)}%
            </span>
          </div>
        )}
      </div>

      {/* Main Content */}
      <div style={{ marginTop: '32px', display: 'grid', gridTemplateColumns: '1fr', gap: '24px' }} className="lg:grid-cols-3 lg:gap-8">
        {/* Resources */}
        <div className="reveal lg:col-span-2" data-delay="2">
          <div className="border border-[var(--border)]">
            <div className="flex flex-wrap gap-0 border-b border-[var(--border)]">
              {resourceTabs.map((tab) => {
                const Icon = tab.icon
                const count = tab.value === 'all' 
                  ? resources?.length || 0 
                  : (resourcesByType[tab.value] || []).length
                return (
                  <button
                    key={tab.value}
                    onClick={() => setActiveTab(tab.value)}
                    className={`flex items-center gap-2 border-r border-[var(--border)] px-4 py-3 text-sm transition-all hover:bg-[var(--surface)] hover:text-[var(--fg)] ${
                      activeTab === tab.value
                        ? 'bg-[var(--surface)] text-[var(--fg)]'
                        : 'text-[var(--muted)]'
                    }`}
                  >
                    <Icon className="h-4 w-4" />
                    <span>{tab.label}</span>
                    {count > 0 && (
                      <span className="font-[var(--font-mono)] text-[0.625rem] text-[var(--accent)]" style={{ fontFamily: 'var(--font-mono)' }}>
                        {count}
                      </span>
                    )}
                  </button>
                )
              })}
            </div>

            <div className="p-6">
              {filteredResources.length > 0 ? (
                <div className="space-y-0">
                  {filteredResources.map((resource: Resource) => (
                    <div
                      key={resource.id}
                      className="flex items-start gap-4 border-b border-[var(--border)] p-4 last:border-b-0 transition-all hover:bg-[var(--surface)]"
                    >
                      <ResourceTypeIcon type={resource.type} className="mt-1 h-5 w-5 flex-shrink-0 text-[var(--accent)]" />
                      <div className="flex-1">
                        <a
                          href={resource.url || '#'}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-[var(--fg)] transition-colors hover:text-[var(--accent)]"
                        >
                          {resource.title}
                        </a>
                        {resource.content && (
                          <p className="mt-1 text-sm text-[var(--muted)] line-clamp-2">
                            {resource.content}
                          </p>
                        )}
                        <div className="mt-2 flex items-center gap-3">
                          <span className="badge-editorial">
                            {resource.type.replace(/_/g, ' ')}
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center py-12 text-center">
                  <BookOpen className="h-12 w-12 text-[var(--muted)] opacity-30" />
                  <p className="mt-4 text-[var(--muted)]">No resources available yet.</p>
                </div>
              )}
            </div>
          </div>
        </div>

      </div>

      {/* Recommendations */}
      <div className="reveal mt-8" data-delay="3">
        <RecommendedTopics topicId={topicId} />
      </div>
    </div>
  )
}
