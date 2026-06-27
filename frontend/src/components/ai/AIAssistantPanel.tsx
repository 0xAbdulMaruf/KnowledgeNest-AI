import { useState, useRef, useEffect } from 'react'
import { Send, Sparkles, HelpCircle, ListChecks, FileText, BookOpen } from 'lucide-react'
import { useChatWithAI } from '@/hooks/use-api'

interface AIAssistantPanelProps {
  topicId?: number | null
  topicName?: string
}

const quickActions = [
  { label: 'Explain', icon: Sparkles, prompt: 'Explain this topic in detail' },
  { label: 'Quiz Me', icon: HelpCircle, prompt: 'Create a quiz on this topic' },
  { label: 'MCQ', icon: ListChecks, prompt: 'Generate MCQ questions' },
  { label: 'Summarize', icon: FileText, prompt: 'Summarize the key points' },
]

export default function AIAssistantPanel({ topicId, topicName }: AIAssistantPanelProps) {
  const [messages, setMessages] = useState<{ role: 'user' | 'ai'; content: string }[]>([])
  const [input, setInput] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const chatMutation = useChatWithAI()

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = async (question: string) => {
    if (!question.trim()) return

    setMessages((prev) => [...prev, { role: 'user', content: question }])
    setInput('')

    try {
      const response = await chatMutation.mutateAsync({ topicId, question })
      setMessages((prev) => [...prev, { role: 'ai', content: response.answer || 'No response' }])
    } catch {
      setMessages((prev) => [...prev, { role: 'ai', content: 'Sorry, I encountered an error. Please try again.' }])
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    sendMessage(input)
  }

  return (
    <div className="flex h-full flex-col bg-[var(--bg)]">
      {/* Header */}
      <div className="flex items-center gap-3 border-b border-[var(--border)] px-4 py-3">
        <Sparkles className="h-4 w-4 text-[var(--accent)]" />
        <div>
          <h3 className="text-sm font-medium text-[var(--fg)]">AI Assistant</h3>
          {topicName && (
            <p className="font-[var(--font-mono)] text-[0.625rem] uppercase tracking-[0.1em] text-[var(--muted)]" style={{ fontFamily: 'var(--font-mono)' }}>
              {topicName}
            </p>
          )}
          {!topicName && (
            <p className="font-[var(--font-mono)] text-[0.625rem] uppercase tracking-[0.1em] text-[var(--muted)]" style={{ fontFamily: 'var(--font-mono)' }}>
              General Study Mode
            </p>
          )}
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-auto p-4">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <BookOpen className="h-10 w-10 text-[var(--muted)] opacity-30" />
            <p className="mt-4 text-sm text-[var(--muted)]">
              {topicName ? 'Ask me anything about this topic' : 'Ask me anything about your studies'}
            </p>
            <div className="mt-6 grid grid-cols-2 gap-2 w-full">
              {quickActions.map((action) => {
                const Icon = action.icon
                return (
                  <button
                    key={action.label}
                    onClick={() => sendMessage(action.prompt)}
                    className="flex items-center gap-2 border border-[var(--border)] p-3 text-xs text-[var(--muted)] transition-all hover:border-[var(--accent)] hover:text-[var(--fg)]"
                  >
                    <Icon className="h-3.5 w-3.5" />
                    {action.label}
                  </button>
                )
              })}
            </div>
          </div>
        )}

        {messages.map((msg, i) => (
          <div
            key={i}
            className={`mb-4 flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[85%] px-4 py-3 text-sm ${
                msg.role === 'user'
                  ? 'bg-[var(--accent)] text-[var(--bg)]'
                  : 'border border-[var(--border)] text-[var(--fg)]'
              }`}
            >
              <p className="whitespace-pre-wrap leading-relaxed">{msg.content}</p>
            </div>
          </div>
        ))}

        {chatMutation.isPending && (
          <div className="flex justify-start">
            <div className="border border-[var(--border)] px-4 py-3">
              <div className="flex items-center gap-2">
                <div className="h-1.5 w-1.5 animate-pulse bg-[var(--accent)]" />
                <div className="h-1.5 w-1.5 animate-pulse bg-[var(--accent)]" style={{ animationDelay: '0.15s' }} />
                <div className="h-1.5 w-1.5 animate-pulse bg-[var(--accent)]" style={{ animationDelay: '0.3s' }} />
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="border-t border-[var(--border)] p-3">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question..."
            className="flex-1 border border-[var(--border)] bg-[var(--bg)] px-3 py-2 text-sm text-[var(--fg)] placeholder-[var(--muted)] outline-none transition-colors focus:border-[var(--accent)]"
          />
          <button
            type="submit"
            disabled={chatMutation.isPending || !input.trim()}
            className="flex items-center justify-center bg-[var(--accent)] px-3 py-2 text-[var(--bg)] transition-opacity hover:opacity-90 disabled:opacity-40"
          >
            <Send className="h-4 w-4" />
          </button>
        </div>
      </form>
    </div>
  )
}
