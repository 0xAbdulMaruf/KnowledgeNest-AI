import { memo, type MouseEvent } from 'react'

interface MarkdownProps {
  content: string
  className?: string
  onCodeAction?: (action: string, code: string, language: string) => void
}

function escapeHtml(value: string): string {
  return value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;')
}

function inlineMarkdown(value: string): string {
  let html = escapeHtml(value)
  html = html.replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer" class="text-[var(--accent)] underline underline-offset-2 hover:opacity-80">$1</a>')
  html = html.replace(/`([^`]+)`/g, '<code class="rounded-md bg-[var(--surface)] px-1.5 py-0.5 font-[var(--font-mono)] text-[0.85em] text-[var(--accent)]">$1</code>')
  html = html.replace(/\*\*([^*]+)\*\*/g, '<strong class="font-semibold text-[var(--fg)]">$1</strong>')
  html = html.replace(/__([^_]+)__/g, '<strong class="font-semibold text-[var(--fg)]">$1</strong>')
  html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>')
  html = html.replace(/_([^_]+)_/g, '<em>$1</em>')
  return html
}

function isTableSeparator(line: string): boolean {
  const cells = line.trim().replace(/^\|/, '').replace(/\|$/, '').split('|')
  return cells.length >= 2 && cells.every((cell) => /^\s*:?-{3,}:?\s*$/.test(cell))
}

function tableHtml(headerLine: string, body: string[]): string {
  const split = (line: string) => line.trim().replace(/^\|/, '').replace(/\|$/, '').split('|').map((cell) => cell.trim())
  const headers = split(headerLine)
  const rows = body.map(split)
  return `<div class="my-4 overflow-x-auto rounded-lg border border-[var(--border)]"><table class="w-full min-w-[420px] border-collapse text-left text-[0.9em]"><thead class="bg-[var(--surface)]"><tr>${headers.map((cell) => `<th class="border-b border-[var(--border)] px-3 py-2 font-semibold text-[var(--fg)]">${inlineMarkdown(cell)}</th>`).join('')}</tr></thead><tbody>${rows.map((row) => `<tr class="even:bg-[var(--surface)]/60">${headers.map((_, index) => `<td class="border-b border-[var(--border)] px-3 py-2 align-top">${inlineMarkdown(row[index] || '')}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`
}

function codeToolbar(code: string, language: string, blockNumber: number): string {
  const encodedCode = encodeURIComponent(code)
  const label = language || 'Code'
  return `<div class="markdown-code-toolbar"><span class="markdown-code-language">${escapeHtml(label)}</span><div class="markdown-code-actions"><button type="button" class="markdown-code-action" data-code-action="copy" data-code="${encodedCode}" data-language="${escapeHtml(language)}" title="Copy code">Copy</button><button type="button" class="markdown-code-action" data-code-action="download" data-code="${encodedCode}" data-language="${escapeHtml(language)}" data-block-number="${blockNumber}" title="Download code">Download</button><button type="button" class="markdown-code-action" data-code-action="explain" data-code="${encodedCode}" data-language="${escapeHtml(language)}" title="Ask AI to explain this code">Explain</button></div></div>`
}

function parseMarkdown(text: string): string {
  const lines = text.replace(/\r\n?/g, '\n').split('\n')
  const blocks: string[] = []
  let paragraph: string[] = []
  let listType: 'ul' | 'ol' | null = null
  let listItems: string[] = []
  let quoteLines: string[] = []
  let codeLines: string[] = []
  let codeLanguage = ''
  let codeBlockNumber = 0
  let inCode = false

  const flushParagraph = () => {
    if (paragraph.length) {
      blocks.push(`<p>${paragraph.map(inlineMarkdown).join('<br />')}</p>`)
      paragraph = []
    }
  }
  const flushList = () => {
    if (listType && listItems.length) {
      blocks.push(`<${listType} class="my-3 space-y-1 pl-6 ${listType === 'ol' ? 'list-decimal' : 'list-disc'}">${listItems.map((item) => `<li class="pl-1">${inlineMarkdown(item)}</li>`).join('')}</${listType}>`)
    }
    listType = null
    listItems = []
  }
  const flushQuote = () => {
    if (quoteLines.length) {
      blocks.push(`<blockquote class="my-4 border-l-2 border-[var(--accent)] bg-[var(--surface)]/60 px-4 py-2 text-[var(--muted)]">${quoteLines.map(inlineMarkdown).join('<br />')}</blockquote>`)
      quoteLines = []
    }
  }
  const flushCode = () => {
    if (inCode) {
      codeBlockNumber += 1
      blocks.push(`<div class="markdown-code-shell"><div class="markdown-code-toolbar-wrap">${codeToolbar(codeLines.join('\n'), codeLanguage, codeBlockNumber)}</div><pre class="markdown-code-block"><code class="font-[var(--font-mono)]" data-language="${escapeHtml(codeLanguage)}">${escapeHtml(codeLines.join('\n'))}</code></pre></div>`)
      codeLines = []
      codeLanguage = ''
      inCode = false
    }
  }

  for (let index = 0; index < lines.length; index += 1) {
    const line = lines[index]
    const trimmed = line.trim()

    if (trimmed.startsWith('```')) {
      flushParagraph(); flushList(); flushQuote()
      if (inCode) flushCode()
      else {
        inCode = true
        codeLanguage = trimmed.slice(3).trim()
      }
      continue
    }
    if (inCode) {
      codeLines.push(line)
      continue
    }
    if (!trimmed) {
      flushParagraph(); flushList(); flushQuote()
      continue
    }

    if (index + 1 < lines.length && isTableSeparator(lines[index + 1])) {
      flushParagraph(); flushList(); flushQuote()
      const tableBody: string[] = []
      index += 2
      while (index < lines.length && lines[index].trim() && lines[index].includes('|')) {
        tableBody.push(lines[index])
        index += 1
      }
      index -= 1
      blocks.push(tableHtml(line, tableBody))
      continue
    }

    const heading = trimmed.match(/^(#{1,6})\s+(.+)$/)
    if (heading) {
      flushParagraph(); flushList(); flushQuote()
      const level = Math.min(heading[1].length, 6)
      blocks.push(`<h${level} class="${level <= 2 ? 'mt-6 text-xl' : 'mt-5 text-lg'} font-semibold tracking-tight text-[var(--fg)]">${inlineMarkdown(heading[2])}</h${level}>`)
      continue
    }
    if (/^(---|___|\*\*\*)$/.test(trimmed)) {
      flushParagraph(); flushList(); flushQuote()
      blocks.push('<hr class="my-5 border-[var(--border)]" />')
      continue
    }
    const quote = trimmed.match(/^>\s?(.*)$/)
    if (quote) {
      flushParagraph(); flushList()
      quoteLines.push(quote[1])
      continue
    }
    const list = trimmed.match(/^([-*+] |\d+[.)] )(.*)$/)
    if (list) {
      flushParagraph(); flushQuote()
      const nextType = /^\d/.test(list[1]) ? 'ol' : 'ul'
      if (listType && listType !== nextType) flushList()
      listType = nextType
      listItems.push(list[2])
      continue
    }

    flushList(); flushQuote()
    paragraph.push(line)
  }

  flushCode(); flushParagraph(); flushList(); flushQuote()
  return blocks.join('')
}

function Markdown({ content, className = '', onCodeAction }: MarkdownProps) {
  const handleClick = async (event: MouseEvent<HTMLDivElement>) => {
    const target = event.target as HTMLElement
    const button = target.closest<HTMLButtonElement>('[data-code-action]')
    if (!button) return
    const code = decodeURIComponent(button.dataset.code || '')
    const language = button.dataset.language || ''
    const action = button.dataset.codeAction || ''
    const blockNumber = button.dataset.blockNumber || '1'
    if (!code) return

    if (action === 'copy') {
      try {
        let copied = false
        if (navigator.clipboard?.writeText) {
          try {
            await navigator.clipboard.writeText(code)
            copied = true
          } catch {
            // Fall through to the legacy copy path on insecure/local origins.
          }
        }
        if (!copied) {
          const textarea = document.createElement('textarea')
          textarea.value = code
          textarea.setAttribute('readonly', '')
          textarea.style.position = 'fixed'
          textarea.style.opacity = '0'
          document.body.appendChild(textarea)
          try {
            textarea.select()
            copied = document.execCommand('copy')
          } finally {
            textarea.remove()
          }
        }
        if (!copied) throw new Error('Clipboard copy was not available')
        const original = button.textContent || 'Copy'
        button.textContent = 'Copied!'
        window.setTimeout(() => { button.textContent = original }, 1600)
      } catch {
        button.textContent = 'Copy failed'
        window.setTimeout(() => { button.textContent = 'Copy' }, 1600)
      }
      return
    }
    if (action === 'download') {
      const extensionMap: Record<string, string> = { javascript: 'js', js: 'js', typescript: 'ts', ts: 'ts', python: 'py', py: 'py', java: 'java', cpp: 'cpp', 'c++': 'cpp', c: 'c', html: 'html', css: 'css', json: 'json', bash: 'sh', shell: 'sh', sh: 'sh', sql: 'sql' }
      const safeLanguage = language.toLowerCase().replace(/[^a-z0-9+#-]/g, '') || 'code'
      const extension = extensionMap[safeLanguage] || 'txt'
      let hash = 0
      for (let index = 0; index < code.length; index += 1) hash = ((hash << 5) - hash + code.charCodeAt(index)) | 0
      const suffix = Math.abs(hash).toString(36).slice(0, 6) || 'snippet'
      const blob = new Blob([code], { type: 'text/plain;charset=utf-8' })
      const url = URL.createObjectURL(blob)
      const anchor = document.createElement('a')
      anchor.href = url
      anchor.download = `knowledgenest-${safeLanguage}-${blockNumber}-${suffix}-${Date.now()}.${extension}`
      document.body.appendChild(anchor)
      anchor.click()
      anchor.remove()
      window.setTimeout(() => URL.revokeObjectURL(url), 1000)
      return
    }
    onCodeAction?.(action, code, language)
  }

  return (
    <div
      onClick={handleClick}
      className={`markdown-content text-sm leading-relaxed text-[var(--fg)] ${className}`}
      dangerouslySetInnerHTML={{ __html: parseMarkdown(content) }}
    />
  )
}

export default memo(Markdown)
