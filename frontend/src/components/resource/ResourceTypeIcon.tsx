import { BookOpen, FileText, Video, FileQuestion, Dumbbell, BookMarked, Link as LinkIcon, Code, File, Image, HelpCircle } from 'lucide-react'
import type { ResourceType } from '@/services/api'

interface ResourceTypeIconProps {
  type: ResourceType | string
  className?: string
}

const iconMap: Record<string, typeof BookOpen> = {
  college_notes: BookOpen,
  external_notes: FileText,
  pdf: File,
  video: Video,
  pyq: FileQuestion,
  important_questions: HelpCircle,
  practice_questions: Dumbbell,
  coding_problems: Code,
  assignment: FileText,
  book: BookMarked,
  documentation: LinkIcon,
  image: Image,
}

export default function ResourceTypeIcon({ type, className }: ResourceTypeIconProps) {
  const Icon = iconMap[type] || FileText
  return <Icon className={className} />
}
