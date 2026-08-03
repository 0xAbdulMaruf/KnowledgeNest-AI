import axios from 'axios'
import { useEffect, useMemo, useRef, useState, type FormEvent, type KeyboardEvent as ReactKeyboardEvent } from 'react'
import { ArrowDown, BookOpen, Bug, Check, Code, Copy, Download, FileText, Globe, GraduationCap, HelpCircle, Layers, Lightbulb, ListChecks, Pencil, Plus, RotateCcw, Search, Send, Share2, Sparkles, Square, StickyNote, ThumbsDown, ThumbsUp, Trash2 } from 'lucide-react'
import { useStreamChatWithAI } from '@/hooks/use-api'
import { AI_DEVELOPER_CONFIG_KEY } from '@/services/api'
import type { AIProviderConfig } from '@/services/api'
import Markdown from '@/components/ui/markdown'

type ContextScope = 'topic' | 'unit' | 'subject' | 'general'

const scopeOptions: { value: ContextScope; label: string; icon: typeof Sparkles }[] = [
  { value: 'topic', label: 'This Topic', icon: Sparkles },
  { value: 'unit', label: 'This Unit', icon: Layers },
  { value: 'subject', label: 'This Subject', icon: GraduationCap },
  { value: 'general', label: 'General', icon: Globe },
]

interface AIAssistantPanelProps {
  topicId?: number | null
  topicName?: string
  topicDescription?: string
  topicTags?: string[]
}

type QuickAction = { label: string; icon: typeof Sparkles; mode: string; prompt: string }

const generalPrompts: QuickAction[] = [
  { label: 'Explain', icon: Sparkles, mode: 'explain_topic', prompt: 'Explain this topic in detail' },
  { label: 'Quiz Me', icon: HelpCircle, mode: 'generate_quiz', prompt: 'Create a quiz on this topic' },
  { label: 'MCQ', icon: ListChecks, mode: 'generate_mcq', prompt: 'Generate MCQ questions' },
  { label: 'Summarize', icon: FileText, mode: 'answer_question', prompt: 'Summarize the key points' },
]

const generalNoTopicPrompts: QuickAction[] = [
  { label: 'Learn', icon: BookOpen, mode: 'answer_question', prompt: 'Based on my syllabus, suggest a topic to study today and explain why it is important. Start by briefly listing 2-3 options from the curriculum and ask me which one I want to explore.' },
  { label: 'Notes', icon: StickyNote, mode: 'answer_question', prompt: 'I need revision notes. Ask me which subject or topic from my syllabus I should focus on, then help me create concise revision notes for that topic.' },
  { label: 'Quick Start', icon: Lightbulb, mode: 'answer_question', prompt: 'Pick an important topic from my curriculum and give me a quick 5-minute introduction. Start by suggesting one high-priority topic from the context.' },
  { label: 'Find Topic', icon: Search, mode: 'answer_question', prompt: 'List 3-4 subjects from the curriculum context and ask me which one I want to study. Then suggest a unit or topic to start with.' },
]

const codePatterns = /^(python|c\+\+|c-programming|c\b|java|javascript|typescript|rust|go|ruby|php|swift|kotlin|programming|coding|algorithm|data structure|oops?|object.oriented)/i
const codeTagPatterns = /(python|c\+\+|c-programming|java|javascript|typescript|rust|golang|ruby|php|swift|kotlin|programming|coding|algorithm|data-structures|oops?|object-oriented|compiler|syntax|debugging)/i
const mathPatterns = /(math|calculus|algebra|statistics|probability|linear|discrete|numerical|geometry|trigonometry)/i
const theoryPatterns = /(history|theory|principle|concept|introduction|overview|fundamentals?|architecture)/i

function getTopicPrompts(topicName?: string, topicDescription?: string, topicTags?: string[]): QuickAction[] {
  if (!topicName) return generalNoTopicPrompts

  const name = topicName.toLowerCase()
  const desc = (topicDescription || '').toLowerCase()
  const tags = (topicTags || []).join(' ').toLowerCase()
  const fullText = `${name} ${desc} ${tags}`

  const isCodeTopic = codePatterns.test(name) || codeTagPatterns.test(tags) || codePatterns.test(desc)
  const isMathTopic = mathPatterns.test(fullText) && !isCodeTopic
  const isTheoryTopic = theoryPatterns.test(fullText) && !isCodeTopic

  if (isCodeTopic) {
    return [
      { label: 'Explain', icon: Sparkles, mode: 'explain_topic', prompt: `Explain ${topicName} clearly with simple code examples` },
      { label: 'Code', icon: Code, mode: 'answer_question', prompt: `Write a complete, well-commented ${topicName} example with explanation` },
      { label: 'Debug', icon: Bug, mode: 'answer_question', prompt: `Show common mistakes and bugs when working with ${topicName} and how to fix them` },
      { label: 'Quiz Me', icon: HelpCircle, mode: 'generate_quiz', prompt: `Create a quiz on ${topicName}` },
    ]
  }

  if (isMathTopic) {
    return [
      { label: 'Explain', icon: Sparkles, mode: 'explain_topic', prompt: `Explain ${topicName} step by step with worked examples` },
      { label: 'Solve', icon: Lightbulb, mode: 'answer_question', prompt: `Walk me through solving a ${topicName} problem from start to finish` },
      { label: 'Formula', icon: FileText, mode: 'answer_question', prompt: `List the key formulas and concepts for ${topicName} with examples` },
      { label: 'Quiz Me', icon: HelpCircle, mode: 'generate_quiz', prompt: `Create a quiz on ${topicName}` },
    ]
  }

  if (isTheoryTopic) {
    return [
      { label: 'Overview', icon: Sparkles, mode: 'explain_topic', prompt: `Give me a comprehensive overview of ${topicName}` },
      { label: 'Key Points', icon: Lightbulb, mode: 'answer_question', prompt: `List the most important concepts and takeaways for ${topicName}` },
      { label: 'Compare', icon: FileText, mode: 'answer_question', prompt: `Compare ${topicName} with related concepts and explain the differences` },
      { label: 'Quiz Me', icon: HelpCircle, mode: 'generate_quiz', prompt: `Create a quiz on ${topicName}` },
    ]
  }

  return generalPrompts
}

type ChatMessage = {
  id: number
  role: 'user' | 'ai'
  content: string
  isTyping?: boolean
}

const conversationStoragePrefix = 'kn-ai-conversation'

function getConversationStorageKey(topicId?: number | null): string {
  return `${conversationStoragePrefix}:${topicId ? `topic:${topicId}` : 'general'}`
}

function loadConversation(key: string): ChatMessage[] {
  try {
    const raw = sessionStorage.getItem(key)
    if (!raw) return []
    const parsed = JSON.parse(raw) as unknown
    if (!Array.isArray(parsed)) return []
    return parsed
      .filter((message): message is ChatMessage => (
        typeof message === 'object'
        && message !== null
        && typeof (message as ChatMessage).id === 'number'
        && ((message as ChatMessage).role === 'user' || (message as ChatMessage).role === 'ai')
        && typeof (message as ChatMessage).content === 'string'
      ))
      .slice(-100)
      .map((message, index) => ({
        ...message,
        id: index + 1,
        isTyping: undefined,
        content: message.content || (message.role === 'ai' ? 'Response stopped before completion.' : message.content),
      }))
  } catch {
    return []
  }
}

function saveConversation(key: string, messages: ChatMessage[]): void {
  try {
    if (!messages.length) {
      sessionStorage.removeItem(key)
      return
    }
    sessionStorage.setItem(key, JSON.stringify(messages.slice(-100)))
  } catch {
    // Storage can be unavailable or full; chat should continue in memory.
  }
}

function loadDeveloperConfig(): AIProviderConfig | undefined {
  try {
    const raw = sessionStorage.getItem(AI_DEVELOPER_CONFIG_KEY)
    if (!raw) return undefined
    const parsed = JSON.parse(raw) as Partial<AIProviderConfig>
    if (!parsed.provider) return undefined
    return { provider: parsed.provider, baseUrl: parsed.baseUrl || '', apiKey: parsed.apiKey || '', model: parsed.model || '', developerToken: parsed.developerToken || '' }
  } catch {
    return undefined
  }
}

function isDeveloperSessionError(error: unknown): boolean {
  return axios.isAxiosError(error) && error.response?.status === 403
}

function getErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const detail = error.response?.data?.detail
    if (typeof detail === 'string' && detail.trim()) return detail
  }
  if (error instanceof Error && error.message.trim()) return error.message
  return 'Sorry, I encountered an error. Please try again.'
}

export default function AIAssistantPanel({ topicId, topicName, topicDescription, topicTags }: AIAssistantPanelProps) {
  const conversationStorageKey = getConversationStorageKey(topicId)
  const [messages, setMessages] = useState<ChatMessage[]>(() => loadConversation(conversationStorageKey))
  const [input, setInput] = useState('')
  const [activeMode, setActiveMode] = useState('answer_question')
  const [editingMessageId, setEditingMessageId] = useState<number | null>(null)
  const [selectedUserMessageId, setSelectedUserMessageId] = useState<number | null>(null)
  const [copiedMessageId, setCopiedMessageId] = useState<number | null>(null)
  const [copyErrorMessageId, setCopyErrorMessageId] = useState<number | null>(null)
  const [feedback, setFeedback] = useState<Record<number, 'up' | 'down'>>({})
  const [scope, setScope] = useState<ContextScope>('topic')
  const [isNearBottom, setIsNearBottom] = useState(true)
  const panelRef = useRef<HTMLDivElement>(null)
  const messagesContainerRef = useRef<HTMLDivElement>(null)
  const composerRef = useRef<HTMLTextAreaElement>(null)
  const messageIdRef = useRef(0)
  const abortControllerRef = useRef<AbortController | null>(null)
  const streamMutation = useStreamChatWithAI()
  const prompts = useMemo(() => getTopicPrompts(topicName, topicDescription, topicTags), [topicName, topicDescription, topicTags])

  const [developerConfig, setDeveloperConfig] = useState<AIProviderConfig | undefined>(() => loadDeveloperConfig())

  useEffect(() => {
    messageIdRef.current = messages.reduce((highestId, message) => Math.max(highestId, message.id), 0)
  }, [])

  useEffect(() => { setScope('topic') }, [topicId])

  useEffect(() => saveConversation(conversationStorageKey, messages), [conversationStorageKey, messages])

  useEffect(() => {
    const syncDeveloperConfig = () => setDeveloperConfig(loadDeveloperConfig())
    window.addEventListener('storage', syncDeveloperConfig)
    window.addEventListener('kn-ai-developer-config-changed', syncDeveloperConfig)
    return () => {
      window.removeEventListener('storage', syncDeveloperConfig)
      window.removeEventListener('kn-ai-developer-config-changed', syncDeveloperConfig)
    }
  }, [])

  useEffect(() => {
    if (!isNearBottom) return
    const container = messagesContainerRef.current
    if (!container) return
    // Scroll the chat viewport itself. scrollIntoView can move the page behind
    // the floating assistant while tokens are arriving.
    const frame = window.requestAnimationFrame(() => {
      container.scrollTop = container.scrollHeight
    })
    return () => window.cancelAnimationFrame(frame)
  }, [messages, isNearBottom])

  useEffect(() => {
    panelRef.current?.focus()
    const panel = panelRef.current
    if (!panel) return
    const handleTab = (event: KeyboardEvent) => {
      if (event.key !== 'Tab') return
      const focusable = Array.from(panel.querySelectorAll<HTMLElement>('button:not([disabled]), textarea:not([disabled]), a[href], [tabindex]:not([tabindex="-1"])'))
      if (!focusable.length) return
      const first = focusable[0]
      const last = focusable[focusable.length - 1]
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus() }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus() }
    }
    panel.addEventListener('keydown', handleTab)
    return () => panel.removeEventListener('keydown', handleTab)
  }, [])

  useEffect(() => () => abortControllerRef.current?.abort(), [])

  useEffect(() => {
    const composer = composerRef.current
    if (!composer) return
    composer.style.height = 'auto'
    composer.style.height = `${Math.min(composer.scrollHeight, 128)}px`
  }, [input])

  const updateScrollPosition = () => {
    const element = messagesContainerRef.current
    if (!element) return
    setIsNearBottom(element.scrollHeight - element.scrollTop - element.clientHeight < 96)
  }

  const scrollToLatest = () => {
    setIsNearBottom(true)
    const container = messagesContainerRef.current
    if (container) container.scrollTo({ top: container.scrollHeight, behavior: 'smooth' })
  }

  const stopStreaming = () => {
    abortControllerRef.current?.abort()
    abortControllerRef.current = null
  }

  const sendMessage = async (question: string, mode = 'answer_question', conversation = messages) => {
    if (!question.trim() || streamMutation.isPending) return
    const history = conversation.filter((message) => !message.isTyping).map((message) => ({ role: message.role, content: message.content }))
    const userMessageId = ++messageIdRef.current
    const assistantId = ++messageIdRef.current
    setMessages([
      ...conversation,
      { id: userMessageId, role: 'user', content: question.trim() },
      { id: assistantId, role: 'ai', content: '', isTyping: true },
    ])
    setInput('')
    setEditingMessageId(null)
    setSelectedUserMessageId(null)
    setActiveMode(mode)
    setIsNearBottom(true)
    const controller = new AbortController()
    abortControllerRef.current = controller

    try {
      await streamMutation.mutateAsync({
        topicId,
        question: question.trim(),
        mode,
        scope: topicId ? scope : 'general',
        providerConfig: developerConfig,
        history,
        signal: controller.signal,
        callbacks: {
          onChunk: (chunk) => setMessages((previous) => previous.map((message) => message.id === assistantId ? { ...message, content: message.content + chunk } : message)),
          onDone: () => setMessages((previous) => previous.map((message) => message.id === assistantId ? { ...message, isTyping: false } : message)),
        },
      })
      setMessages((previous) => previous.map((message) => message.id === assistantId ? { ...message, isTyping: false } : message))
    } catch (error) {
      if (isDeveloperSessionError(error)) {
        sessionStorage.removeItem(AI_DEVELOPER_CONFIG_KEY)
        setDeveloperConfig(undefined)
        window.dispatchEvent(new Event('kn-ai-developer-config-changed'))
      }
      setMessages((previous) => previous.map((message) => message.id === assistantId ? {
        ...message,
        content: controller.signal.aborted ? (message.content || 'Response stopped.') : isDeveloperSessionError(error) ? 'Developer session expired. Reverted to server AI configuration; please unlock Developer Options again if needed.' : getErrorMessage(error),
        isTyping: false,
      } : message))
    } finally {
      abortControllerRef.current = null
    }
  }

  const copyMessage = async (message: ChatMessage) => {
    try {
      let copied = false
      if (navigator.clipboard?.writeText) {
        try {
          await navigator.clipboard.writeText(message.content)
          copied = true
        } catch {
          // Fall through to the legacy copy path on insecure/local origins.
        }
      }
      if (!copied) {
        const textarea = document.createElement('textarea')
        textarea.value = message.content
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
      setCopyErrorMessageId(null)
      setCopiedMessageId(message.id)
      window.setTimeout(() => setCopiedMessageId((current) => current === message.id ? null : current), 1600)
    } catch {
      setCopiedMessageId(null)
      setCopyErrorMessageId(message.id)
      window.setTimeout(() => setCopyErrorMessageId((current) => current === message.id ? null : current), 1800)
    }
  }

  const regenerate = (messageIndex: number) => {
    const userIndex = [...messages].slice(0, messageIndex).map((message) => message.role).lastIndexOf('user')
    if (userIndex >= 0) sendMessage(messages[userIndex].content, activeMode, messages.slice(0, userIndex))
  }

  const editUserMessage = (message: ChatMessage) => {
    setSelectedUserMessageId(message.id)
    setEditingMessageId(message.id)
    setInput(message.content)
  }

  const startNewConversation = () => {
    stopStreaming()
    setMessages([])
    setInput('')
    setEditingMessageId(null)
    setSelectedUserMessageId(null)
    sessionStorage.removeItem(conversationStorageKey)
  }

  const exportConversation = () => {
    if (!messages.length) return
    const markdown = messages.map((message) => `${message.role === 'user' ? '## You' : '## AI Assistant'}\n\n${message.content}`).join('\n\n---\n\n')
    const blob = new Blob([`# KnowledgeNest AI Conversation\n\n${markdown}\n`], { type: 'text/markdown;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const anchor = document.createElement('a')
    anchor.href = url
    anchor.download = `knowledgenest-conversation-${new Date().toISOString().slice(0, 10)}.md`
    anchor.click()
    URL.revokeObjectURL(url)
  }

  const shareMessage = async (content: string) => {
    try {
      if (navigator.share) await navigator.share({ title: 'KnowledgeNest AI response', text: content })
      else await copyMessage({ id: -1, role: 'ai', content })
    } catch {
      // The share sheet can be dismissed by the user; no error should reach the console.
    }
  }

  const handleCodeAction = (action: string, code: string, language: string) => {
    if (action === 'explain') sendMessage(`Explain this ${language || ''} code carefully. Include what it does, how it works, and any issues:\n\n\`\`\`${language}\n${code}\n\`\`\``)
  }

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault()
    if (!input.trim()) return
    if (editingMessageId !== null) {
      const messageIndex = messages.findIndex((message) => message.id === editingMessageId)
      if (messageIndex >= 0) sendMessage(input, activeMode, messages.slice(0, messageIndex))
      else sendMessage(input, activeMode)
      return
    }
    sendMessage(input, activeMode)
  }

  const handleComposerKeyDown = (event: ReactKeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault()
      event.currentTarget.form?.requestSubmit()
    }
  }

  return (
    <div ref={panelRef} tabIndex={-1} role="region" aria-label="AI Assistant" className="flex h-full flex-col bg-[var(--bg)] outline-none">
      <div className="border-b border-[var(--border)] px-4 py-4 sm:px-5">
        <div className="flex items-start justify-between gap-3">
          <div className="min-w-0">
            <div className="flex items-center gap-2"><Sparkles className="h-4 w-4 text-[var(--accent)]" /><h3 className="text-base font-medium text-[var(--fg)]">AI Assistant</h3></div>
            <p className="mt-1 font-[var(--font-mono)] text-[0.6875rem] uppercase tracking-[0.1em] text-[var(--muted)]" style={{ fontFamily: 'var(--font-mono)' }}>{topicName || 'General Study Mode'}</p>
          </div>
          <div className="flex items-center gap-1">
            <button type="button" onClick={startNewConversation} title="New conversation" aria-label="New conversation" className="chat-icon-button"><Plus className="h-4 w-4" /></button>
            <button type="button" onClick={exportConversation} disabled={!messages.length} title="Export conversation" aria-label="Export conversation" className="chat-icon-button disabled:opacity-30"><Download className="h-4 w-4" /></button>
          </div>
        </div>
        {topicId && (
          <div className="mt-3 flex flex-wrap gap-1">
            {scopeOptions.map((option) => {
              const Icon = option.icon
              const isActive = scope === option.value
              return (
                <button
                  key={option.value}
                  type="button"
                  onClick={() => setScope(option.value)}
                  className={`flex items-center gap-1.5 px-2.5 py-1 text-[0.6875rem] transition-colors ${isActive ? 'bg-[var(--accent)] text-[var(--bg)]' : 'border border-[var(--border)] text-[var(--muted)] hover:text-[var(--fg)]'}`}
                  aria-pressed={isActive}
                  title={`Use ${option.label} as AI context`}
                >
                  <Icon className="h-3 w-3" />
                  {option.label}
                </button>
              )
            })}
          </div>
        )}
      </div>

      <div ref={messagesContainerRef} onScroll={updateScrollPosition} className="relative flex-1 overflow-auto p-4 sm:p-5">
        {messages.length === 0 && (
          <div className="flex h-full flex-col items-center justify-center text-center">
            <BookOpen className="h-10 w-10 text-[var(--muted)] opacity-30" />
            <p className="mt-4 text-base text-[var(--muted)]">{topicName ? 'Ask me anything about this topic' : 'Ask me anything about your studies'}</p>
            <div className="mt-6 grid w-full grid-cols-2 gap-2">
              {prompts.map((action) => { const Icon = action.icon; return <button key={action.label} type="button" onClick={() => sendMessage(action.prompt, action.mode)} className="flex items-center gap-2 border border-[var(--border)] p-3 text-sm text-[var(--muted)] transition-all hover:border-[var(--accent)] hover:text-[var(--fg)]"><Icon className="h-4 w-4" />{action.label}</button> })}
            </div>
          </div>
        )}

        {messages.map((message, messageIndex) => (
          <div
            key={message.id}
            className={`mb-5 flex ${message.role === 'user' ? 'cursor-pointer justify-end' : 'justify-start'}`}
            onClick={() => message.role === 'user' && setSelectedUserMessageId(message.id)}
            onKeyDown={(event) => {
              if (message.role === 'user' && (event.key === 'Enter' || event.key === ' ')) {
                event.preventDefault()
                setSelectedUserMessageId(message.id)
              }
            }}
            tabIndex={message.role === 'user' ? 0 : undefined}
            role={message.role === 'user' ? 'button' : undefined}
            aria-label={message.role === 'user' ? 'Select your question to show actions' : undefined}
          >
            <div className={`max-w-[90%] px-4 py-3 text-[15px] sm:max-w-[85%] ${message.role === 'user' ? `bg-[var(--accent)] text-[var(--bg)] ${selectedUserMessageId === message.id ? 'ring-2 ring-[var(--accent)]/50 ring-offset-2 ring-offset-[var(--bg)]' : ''}` : 'border border-[var(--border)] text-[var(--fg)]'}`}>
              {message.role === 'ai' ? (message.content ? <Markdown content={message.content} onCodeAction={handleCodeAction} className="text-[15px] leading-7 [&_p]:my-3 [&_li]:my-1.5 [&_strong]:font-semibold" /> : <span className="text-[var(--muted)]">Thinking…</span>) : <p className="whitespace-pre-wrap leading-7">{message.content}</p>}
              {message.role === 'user' && !message.isTyping && selectedUserMessageId === message.id && <div className="mt-2 flex justify-end border-t border-black/10 pt-2"><button type="button" onClick={(event) => { event.stopPropagation(); editUserMessage(message) }} aria-label="Edit question" title="Edit question" className="chat-action-button"><Pencil className="h-3.5 w-3.5" /> Edit</button></div>}
              {message.role === 'ai' && !message.isTyping && message.content && (
                <div className="mt-4 flex flex-wrap items-center gap-x-3 gap-y-2 border-t border-[var(--border)] pt-2">
                  <button type="button" onClick={() => copyMessage(message)} aria-label="Copy response" className={`chat-action-button ${copyErrorMessageId === message.id ? 'text-red-500' : ''}`}>{copiedMessageId === message.id ? <Check className="h-3.5 w-3.5 text-[var(--accent-2)]" /> : <Copy className="h-3.5 w-3.5" />}{copiedMessageId === message.id ? 'Copied' : copyErrorMessageId === message.id ? 'Copy failed' : 'Copy'}</button>
                  <button type="button" onClick={() => regenerate(messageIndex)} aria-label="Regenerate response" className="chat-action-button"><RotateCcw className="h-3.5 w-3.5" /> Retry</button>
                  <button type="button" onClick={() => shareMessage(message.content)} aria-label="Share response" className="chat-action-button"><Share2 className="h-3.5 w-3.5" /> Share</button>
                  <button type="button" onClick={() => setFeedback((previous) => ({ ...previous, [message.id]: 'up' }))} aria-label="Helpful response" className={`chat-action-button ${feedback[message.id] === 'up' ? 'text-[var(--accent)]' : ''}`}><ThumbsUp className="h-3.5 w-3.5" /></button>
                  <button type="button" onClick={() => setFeedback((previous) => ({ ...previous, [message.id]: 'down' }))} aria-label="Unhelpful response" className={`chat-action-button ${feedback[message.id] === 'down' ? 'text-red-500' : ''}`}><ThumbsDown className="h-3.5 w-3.5" /></button>
                </div>
              )}
            </div>
          </div>
        ))}
        {streamMutation.isPending && <div className="flex justify-start"><div className="border border-[var(--border)] px-4 py-3 text-sm text-[var(--muted)]">Generating response…</div></div>}
        {!isNearBottom && <button type="button" onClick={scrollToLatest} className="chat-jump-button" aria-label="Jump to latest message"><ArrowDown className="h-4 w-4" /> Latest</button>}
      </div>

      <div className="flex items-center justify-between border-t border-[var(--border)] px-3 pt-2 sm:px-4">
        <button type="button" onClick={startNewConversation} disabled={!messages.length} className="flex items-center gap-1 text-sm text-[var(--muted)] hover:text-red-500 disabled:opacity-30"><Trash2 className="h-3.5 w-3.5" /> Clear</button>
        {streamMutation.isPending && <button type="button" onClick={stopStreaming} className="flex items-center gap-1 text-sm text-[var(--muted)] hover:text-[var(--accent)]"><Square className="h-3.5 w-3.5" /> Stop</button>}
      </div>
      <form onSubmit={handleSubmit} className="border-t border-[var(--border)] p-3 sm:p-4">
        <div className="flex items-end gap-2 rounded-xl border border-[var(--border)] bg-[var(--surface)] p-1.5 focus-within:border-[var(--accent)]">
          <textarea ref={composerRef} aria-label="Ask the AI assistant" value={input} onChange={(event) => setInput(event.target.value)} onKeyDown={handleComposerKeyDown} placeholder={editingMessageId !== null ? 'Edit your question…' : 'Ask a question… (Shift+Enter for a new line)'} disabled={streamMutation.isPending} rows={1} className="max-h-32 min-h-10 flex-1 resize-none overflow-y-auto bg-transparent px-2 py-2 text-[15px] leading-6 text-[var(--fg)] placeholder-[var(--muted)] outline-none disabled:opacity-40" />
          <button type="submit" disabled={streamMutation.isPending || !input.trim()} aria-label="Send message" className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-[var(--accent)] text-[var(--bg)] transition-opacity hover:opacity-90 disabled:opacity-40"><Send className="h-4 w-4" /></button>
        </div>
        <p className="mt-2 text-center text-[0.6875rem] text-[var(--muted)]">Enter to send · Shift+Enter for a new line</p>
      </form>
    </div>
  )
}
