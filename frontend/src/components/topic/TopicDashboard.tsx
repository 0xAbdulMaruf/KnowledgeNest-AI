import { useTopicResources } from '@/hooks/use-api'
import { Skeleton } from '@/components/ui/skeleton'
import ResourceList from './ResourceList'
import type { ResourceType } from '@/services/api'

interface TopicDashboardProps {
  topicId: number
  activeTab?: string
}

export default function TopicDashboard({ topicId, activeTab = 'all' }: TopicDashboardProps) {
  const typeFilter = activeTab === 'all' ? undefined : (activeTab as ResourceType)
  const { data: resources, isLoading } = useTopicResources(topicId, typeFilter)

  if (isLoading) {
    return (
      <div className="space-y-3">
        {Array.from({ length: 3 }).map((_, i) => (
          <Skeleton key={i} className="h-16" />
        ))}
      </div>
    )
  }

  return <ResourceList resources={resources || []} />
}
