import { Link } from 'react-router-dom'
import { BookOpen } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import type { Subject } from '@/services/api'

interface SubjectCardProps {
  subject: Subject
}

export default function SubjectCard({ subject }: SubjectCardProps) {
  return (
    <Link to={`/subjects/${subject.id}`}>
      <Card className="group h-full">
        <CardHeader>
          <div className="flex items-start justify-between">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-[var(--accent)]/10 text-[var(--accent)] group-hover:bg-[var(--accent)]/20 transition-colors">
              <BookOpen className="h-[18px] w-[18px]" />
            </div>
            {subject.code && (
              <Badge variant="outline" className="text-[11px]">{subject.code}</Badge>
            )}
          </div>
          <CardTitle className="mt-3 line-clamp-2 text-sm group-hover:text-[var(--accent)] transition-colors">
            {subject.name}
          </CardTitle>
        </CardHeader>
        <CardContent>
          {subject.semester_number && (
            <p className="mb-3 text-xs text-[var(--muted)]">
              Semester {subject.semester_number}
            </p>
          )}
          {subject.tags && subject.tags.length > 0 && (
            <div className="flex flex-wrap gap-1.5">
              {subject.tags.slice(0, 3).map((tag) => (
                <Badge key={tag} variant="secondary" className="text-[11px]">
                  {tag}
                </Badge>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </Link>
  )
}
