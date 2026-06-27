import { ExternalLink } from 'lucide-react'
import ResourceTypeIcon from '@/components/resource/ResourceTypeIcon'
import type { Resource } from '@/services/api'

interface ResourceListProps {
  resources: Resource[]
}

const typeLabels: Record<string, string> = {
  college_notes: 'College Notes',
  external_notes: 'External Notes',
  pdf: 'PDF',
  video: 'Video',
  pyq: 'PYQ',
  important_questions: 'Important Questions',
  practice_questions: 'Practice Questions',
  coding_problems: 'Coding Problems',
  assignment: 'Assignment',
  book: 'Book',
  documentation: 'Documentation',
  image: 'Image',
}

export default function ResourceList({ resources }: ResourceListProps) {
  if (!resources || resources.length === 0) {
    return (
      <div className="border border-[var(--border)] p-8 text-center">
        <p className="text-sm text-[var(--muted)]">No resources available.</p>
      </div>
    )
  }

  const grouped = resources.reduce((acc, resource) => {
    if (!acc[resource.type]) acc[resource.type] = []
    acc[resource.type].push(resource)
    return acc
  }, {} as Record<string, Resource[]>)

  return (
    <div className="space-y-0">
      {Object.entries(grouped).map(([type, items]) => (
        <div key={type}>
          <h3 className="flex items-center gap-2 border-b border-[var(--border)] px-4 py-3 font-[var(--font-mono)] text-xs uppercase tracking-[0.1em] text-[var(--muted)]" style={{ fontFamily: 'var(--font-mono)' }}>
            <ResourceTypeIcon type={type} className="h-4 w-4" />
            {typeLabels[type] || type} ({items.length})
          </h3>
          <div>
            {items.map((resource) => (
              <div
                key={resource.id}
                className="flex items-center justify-between border-b border-[var(--border)] px-4 py-3 transition-all last:border-b-0 hover:bg-[var(--surface)]"
              >
                <div className="flex min-w-0 items-center gap-3">
                  <ResourceTypeIcon type={resource.type} className="h-4 w-4 flex-shrink-0 text-[var(--accent)]" />
                  <div className="min-w-0">
                    <p className="truncate text-sm text-[var(--fg)]">{resource.title}</p>
                    {resource.content && (
                      <p className="mt-1 truncate text-xs text-[var(--muted)]">{resource.content}</p>
                    )}
                  </div>
                </div>
                {resource.url && (
                  <a
                    href={resource.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex flex-shrink-0 items-center gap-1 font-[var(--font-mono)] text-xs text-[var(--accent)] transition-colors hover:text-[#4dabff]"
                    style={{ fontFamily: 'var(--font-mono)' }}
                  >
                    Open <ExternalLink className="h-3 w-3" />
                  </a>
                )}
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}
