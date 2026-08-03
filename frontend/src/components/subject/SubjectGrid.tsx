import { useSubjects } from '@/hooks/use-api'
import SubjectCard from './SubjectCard'
import { Skeleton } from '@/components/ui/skeleton'

interface SubjectGridProps {
  semesterId?: number
}

export default function SubjectGrid({ semesterId }: SubjectGridProps) {
  const { data: subjects, isLoading, error } = useSubjects(semesterId)

  if (isLoading) {
    return (
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {Array.from({ length: 6 }).map((_, i) => (
          <Skeleton key={i} className="h-44" />
        ))}
      </div>
    )
  }

  if (error) {
    return (
      <div className="rounded-lg border border-red-500/30 bg-red-500/5 p-4 text-sm text-red-500">
        Failed to load subjects. Please try again.
      </div>
    )
  }

  if (!subjects || subjects.length === 0) {
    return (
      <div className="rounded-xl border border-[var(--border)] bg-[var(--surface)] p-8 text-center">
        <p className="text-sm text-[var(--muted)]">No subjects found.</p>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {subjects.map((subject) => (
        <SubjectCard key={subject.id} subject={subject} />
      ))}
    </div>
  )
}
