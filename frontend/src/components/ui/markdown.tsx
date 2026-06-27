import { memo } from 'react'

interface MarkdownProps {
  content: string
  className?: string
}

function parseMarkdown(text: string): string {
  let html = text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')

  html = html.replace(/```(\w*)\n([\s\S]*?)```/g, '<pre class="rounded-lg bg-[#f3f4f6] p-4 my-3 overflow-x-auto text-sm"><code>$2</code></pre>')
  html = html.replace(/`([^`]+)`/g, '<code class="rounded bg-[#f3f4f6] px-1.5 py-0.5 text-sm font-mono">$1</code>')
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong class="font-semibold">$1</strong>')
  html = html.replace(/\*(.+?)\*/g, '<em>$1</em>')
  html = html.replace(/^### (.+)$/gm, '<h3 class="text-base font-semibold mt-4 mb-2">$1</h3>')
  html = html.replace(/^## (.+)$/gm, '<h2 class="text-lg font-semibold mt-5 mb-2">$1</h2>')
  html = html.replace(/^# (.+)$/gm, '<h1 class="text-xl font-bold mt-6 mb-3">$1</h1>')
  html = html.replace(/^\* (.+)$/gm, '<li class="ml-4 list-disc">$1</li>')
  html = html.replace(/^- (.+)$/gm, '<li class="ml-4 list-disc">$1</li>')
  html = html.replace(/^\d+\. (.+)$/gm, '<li class="ml-4 list-decimal">$1</li>')
  html = html.replace(/\n\n/g, '</p><p class="mt-2">')
  html = html.replace(/\n/g, '<br/>')

  return `<p>${html}</p>`
}

function Markdown({ content, className = '' }: MarkdownProps) {
  return (
    <div
      className={`prose-sm text-sm leading-relaxed text-[#1a1a1a] ${className}`}
      dangerouslySetInnerHTML={{ __html: parseMarkdown(content) }}
    />
  )
}

export default memo(Markdown)
