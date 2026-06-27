import { Link } from 'react-router-dom'
import { FileText, Star } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import type { Topic } from '@/services/api'

interface TopicCardProps {
  topic: Topic
}

export default function TopicCard({ topic }: TopicCardProps) {
  return (
    <Link to={`/topics/${topic.id}`}>
      <Card className="group h-full">
        <CardHeader>
          <div className="flex items-start justify-between">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-[#f3f4f6] text-[#6b7280] group-hover:bg-[#3b82f6]/10 group-hover:text-[#3b82f6] transition-colors">
              <FileText className="h-[18px] w-[18px]" />
            </div>
            {topic.importance_score && (
              <div className="flex items-center gap-1 text-[#f59e0b]">
                <Star className="h-3.5 w-3.5 fill-current" />
                <span className="text-xs font-semibold">{topic.importance_score.toFixed(1)}</span>
              </div>
            )}
          </div>
          <CardTitle className="mt-3 line-clamp-2 text-sm group-hover:text-[#3b82f6] transition-colors">
            {topic.name}
          </CardTitle>
        </CardHeader>
        <CardContent>
          {topic.unit_name && (
            <p className="mb-3 text-xs text-[#9ca3af]">
              {topic.unit_name}
            </p>
          )}
          <div className="flex flex-wrap gap-1.5">
            {topic.tags?.slice(0, 3).map((tag) => (
              <Badge key={tag} variant="accent" className="text-[11px]">
                {tag}
              </Badge>
            ))}
            {topic.resource_count !== undefined && (
              <Badge variant="outline" className="text-[11px]">
                {topic.resource_count} resources
              </Badge>
            )}
          </div>
        </CardContent>
      </Card>
    </Link>
  )
}
