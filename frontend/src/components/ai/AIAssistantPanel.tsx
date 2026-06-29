import axios from 'axios'
import { useState, useRef, useEffect, useMemo } from 'react'
import { Send, Sparkles, HelpCircle, ListChecks, FileText, BookOpen, ShieldCheck, PlugZap, AlertTriangle } from 'lucide-react'
import { useChatWithAI, useTestAIConnection } from '@/hooks/use-api'
import type { AIProvider, AIProviderConfig } from '@/services/api'
import Markdown from '@/components/ui/markdown'

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

const assistantConfigKey = 'kn-ai-assistant-config'
const assistantVerifiedKey = 'kn-ai-assistant-verified-connection'
const assistantTabsKey = 'kn-ai-assistant-open-tabs'
const assistantTabIdKey = 'kn-ai-assistant-tab-id'
const assistantSessionIdleMs = 60 * 1000

const providerOptions: { value: AIProvider; label: string; description: string }[] = [
  { value: 'local', label: 'Local LLM', description: 'Use the local Ollama model configured on the backend.' },
  { value: 'openai', label: 'OpenAI', description: 'Use OpenAI compatible chat completions.' },
  { value: 'anthropic', label: 'Anthropic', description: 'Use Anthropic messages API.' },
  { value: 'mimo', label: 'Mimo by Xaimoi', description: 'Custom OpenAI-compatible provider.' },
]

const defaultConfig: AIProviderConfig = {
  provider: 'local',
  baseUrl: '',
  apiKey: '',
  model: '',
}

interface VerifiedConnectionRecord {
  configSignature: string
  verifiedAt: number
}

interface OpenTabRecord {
  tabId: string
  lastSeenAt: number
}

function normalizeConfig(config: AIProviderConfig): Required<AIProviderConfig> {
  return {
    provider: config.provider,
    baseUrl: config.baseUrl?.trim() || '',
    apiKey: config.apiKey?.trim() || '',
    model: config.model?.trim() || '',
  }
}

function getConfigSignature(config: AIProviderConfig): string {
  return JSON.stringify(normalizeConfig(config))
}

function getTabId() {
  if (typeof window === 'undefined') return 'server'

  const existing = sessionStorage.getItem(assistantTabIdKey)
  if (existing) return existing

  const next = `${Date.now()}-${Math.random().toString(36).slice(2, 10)}`
  sessionStorage.setItem(assistantTabIdKey, next)
  return next
}

function loadVerifiedConnection(): VerifiedConnectionRecord | null {
  if (typeof window === 'undefined') return null

  try {
    const raw = localStorage.getItem(assistantVerifiedKey)
    if (!raw) return null

    const parsed = JSON.parse(raw) as Partial<VerifiedConnectionRecord>
    if (typeof parsed.configSignature !== 'string' || typeof parsed.verifiedAt !== 'number') {
      return null
    }

    return parsed as VerifiedConnectionRecord
  } catch {
    return null
  }
}

function saveVerifiedConnection(config: AIProviderConfig) {
  if (typeof window === 'undefined') return

  const payload: VerifiedConnectionRecord = {
    configSignature: getConfigSignature(config),
    verifiedAt: Date.now(),
  }
  localStorage.setItem(assistantVerifiedKey, JSON.stringify(payload))
}

function clearVerifiedConnection() {
  if (typeof window === 'undefined') return
  localStorage.removeItem(assistantVerifiedKey)
}

function loadOpenTabs(): OpenTabRecord[] {
  if (typeof window === 'undefined') return []

  try {
    const raw = localStorage.getItem(assistantTabsKey)
    if (!raw) return []

    const parsed = JSON.parse(raw) as OpenTabRecord[]
    return Array.isArray(parsed)
      ? parsed.filter((record) => typeof record.tabId === 'string' && typeof record.lastSeenAt === 'number')
      : []
  } catch {
    return []
  }
}

function persistOpenTabs(nextTabs: OpenTabRecord[]) {
  if (typeof window === 'undefined') return
  localStorage.setItem(assistantTabsKey, JSON.stringify(nextTabs))
}

function registerTab(tabId: string) {
  const now = Date.now()
  const nextTabs = loadOpenTabs().filter((record) => now - record.lastSeenAt < assistantSessionIdleMs)
  const existingIndex = nextTabs.findIndex((record) => record.tabId === tabId)

  if (existingIndex >= 0) {
    nextTabs[existingIndex] = { tabId, lastSeenAt: now }
  } else {
    nextTabs.push({ tabId, lastSeenAt: now })
  }

  persistOpenTabs(nextTabs)
}

function unregisterTab(tabId: string) {
  const nextTabs = loadOpenTabs().filter((record) => record.tabId !== tabId)
  persistOpenTabs(nextTabs)
}

function pruneSessionState() {
  if (typeof window === 'undefined') return

  const now = Date.now()
  const nextTabs = loadOpenTabs().filter((record) => now - record.lastSeenAt < assistantSessionIdleMs)
  if (nextTabs.length === 0) {
    localStorage.removeItem(assistantTabsKey)
    return
  }

  persistOpenTabs(nextTabs)
}

function isVerifiedForConfig(config: AIProviderConfig) {
  if (config.provider === 'local') return true

  const verified = loadVerifiedConnection()
  return verified?.configSignature === getConfigSignature(config)
}

function loadAssistantConfig(): AIProviderConfig {
  if (typeof window === 'undefined') return defaultConfig
  try {
    const raw = localStorage.getItem(assistantConfigKey)
    if (!raw) return defaultConfig
    const parsed = JSON.parse(raw) as Partial<AIProviderConfig>
    return {
      provider: parsed.provider || 'local',
      baseUrl: parsed.baseUrl || '',
      apiKey: parsed.apiKey || '',
      model: parsed.model || '',
    }
  } catch {
    return defaultConfig
  }
}

function getErrorMessage(error: unknown, fallback: string): string {
  if (axios.isAxiosError(error)) {
    const detail = error.response?.data?.detail
    if (typeof detail === 'string' && detail.trim()) {
      return detail
    }
    if (typeof error.message === 'string' && error.message.trim()) {
      return error.message
    }
  }

  if (error instanceof Error && error.message.trim()) {
    return error.message
  }

  return fallback
}

export default function AIAssistantPanel({ topicId, topicName }: AIAssistantPanelProps) {
  const [messages, setMessages] = useState<{ id: number; role: 'user' | 'ai'; content: string; isTyping?: boolean }[]>([])
  const [input, setInput] = useState('')
  const [config, setConfig] = useState<AIProviderConfig>(() => loadAssistantConfig())
  const [connectionState, setConnectionState] = useState<'idle' | 'testing' | 'ready' | 'error'>(() =>
    isVerifiedForConfig(loadAssistantConfig()) ? 'ready' : 'idle'
  )
  const [showSettings, setShowSettings] = useState<boolean>(() => !isVerifiedForConfig(loadAssistantConfig()))
  const [connectionMessage, setConnectionMessage] = useState(() =>
    loadAssistantConfig().provider === 'local' ? 'Local LLM is ready.' : ''
  )
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const typingTimerRef = useRef<number | null>(null)
  const tabIdRef = useRef<string>('')
  const chatMutation = useChatWithAI()
  const testConnectionMutation = useTestAIConnection()

  const providerNeedsTest = config.provider !== 'local'
  const providerLabel = useMemo(
    () => providerOptions.find((option) => option.value === config.provider)?.label || 'Local LLM',
    [config.provider]
  )

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  useEffect(() => {
    return () => {
      if (typingTimerRef.current) {
        window.clearInterval(typingTimerRef.current)
      }
    }
  }, [])

  useEffect(() => {
    if (typeof window === 'undefined') return

    tabIdRef.current = getTabId()
    pruneSessionState()
    registerTab(tabIdRef.current)

    const handleStorage = (event: StorageEvent) => {
      if (event.key === assistantConfigKey) {
        const nextConfig = loadAssistantConfig()
        setConfig(nextConfig)
        if (nextConfig.provider === 'local') {
          setConnectionState('ready')
          setConnectionMessage('Local LLM is ready.')
          setShowSettings(false)
          return
        }

        if (isVerifiedForConfig(nextConfig)) {
          setConnectionState('ready')
          setConnectionMessage('Connection verified for this browser session.')
          setShowSettings(false)
        } else {
          setConnectionState('idle')
          setConnectionMessage('')
          setShowSettings(true)
        }
      }

      if (event.key === assistantVerifiedKey) {
        const currentConfig = loadAssistantConfig()
        if (currentConfig.provider === 'local') {
          setConnectionState('ready')
          setConnectionMessage('Local LLM is ready.')
          setShowSettings(false)
          return
        }

        if (isVerifiedForConfig(currentConfig)) {
          setConnectionState('ready')
          setConnectionMessage('Connection verified for this browser session.')
          setShowSettings(false)
        } else {
          setConnectionState('idle')
          setConnectionMessage('')
          setShowSettings(true)
        }
      }

      if (event.key === assistantTabsKey) {
        pruneSessionState()
      }
    }

    const handleVisibilityChange = () => {
      if (document.visibilityState === 'visible') {
        registerTab(tabIdRef.current)
      }
    }

    window.addEventListener('storage', handleStorage)
    document.addEventListener('visibilitychange', handleVisibilityChange)

    const heartbeat = window.setInterval(() => {
      registerTab(tabIdRef.current)
    }, 15000)

    return () => {
      window.clearInterval(heartbeat)
      window.removeEventListener('storage', handleStorage)
      document.removeEventListener('visibilitychange', handleVisibilityChange)
    }
  }, [])

  useEffect(() => {
    localStorage.setItem(assistantConfigKey, JSON.stringify(config))
    if (config.provider === 'local') {
      clearVerifiedConnection()
      setConnectionState('ready')
      setConnectionMessage('Local LLM is ready.')
      setShowSettings(false)
      return
    }

    if (isVerifiedForConfig(config)) {
      setConnectionState('ready')
      setConnectionMessage('Connection verified for this browser session.')
      setShowSettings(false)
      return
    }

    clearVerifiedConnection()
    setConnectionState('idle')
    setConnectionMessage('')
    setShowSettings(true)
  }, [config])

  const updateConfig = (patch: Partial<AIProviderConfig>) => {
    setConfig((current) => ({ ...current, ...patch }))
    if (config.provider !== 'local') {
      clearVerifiedConnection()
      setConnectionState('idle')
      setConnectionMessage('')
      setShowSettings(true)
    }
  }

  const handleProviderChange = (provider: AIProvider) => {
    const next: AIProviderConfig = {
      ...config,
      provider,
    }

    if (provider === 'local') {
      next.baseUrl = ''
      next.apiKey = ''
      next.model = ''
    } else if (provider === 'openai' && !next.baseUrl) {
      next.baseUrl = 'https://api.openai.com/v1'
    } else if (provider === 'anthropic' && !next.baseUrl) {
      next.baseUrl = 'https://api.anthropic.com/v1'
    }

    setConfig(next)
    clearVerifiedConnection()
    setConnectionState(provider === 'local' ? 'ready' : 'idle')
    setConnectionMessage(provider === 'local' ? 'Local LLM is ready.' : '')
    setShowSettings(provider !== 'local')
  }

  const handleTestConnection = async () => {
    if (!providerNeedsTest) return
    setConnectionState('testing')
    setConnectionMessage('Testing provider connection...')
    try {
      const response = await testConnectionMutation.mutateAsync(config)
      saveVerifiedConnection(config)
      setConnectionState('ready')
      setConnectionMessage(response.message)
      setShowSettings(false)
    } catch (error) {
      const message = getErrorMessage(error, 'Unable to connect')
      clearVerifiedConnection()
      setConnectionState('error')
      setConnectionMessage(message)
    }
  }

  const stopTyping = () => {
    if (typingTimerRef.current) {
      window.clearInterval(typingTimerRef.current)
      typingTimerRef.current = null
    }
  }

  const animateAssistantReply = (fullText: string) => {
    stopTyping()
    const messageId = Date.now() + Math.floor(Math.random() * 1000)
    const text = fullText || 'No response'

    setMessages((prev) => [...prev, { id: messageId, role: 'ai', content: '', isTyping: true }])

    let index = 0
    const step = Math.max(1, Math.ceil(text.length / 140))

    typingTimerRef.current = window.setInterval(() => {
      index = Math.min(index + step, text.length)
      setMessages((prev) =>
        prev.map((message) =>
          message.id === messageId
            ? { ...message, content: text.slice(0, index), isTyping: index < text.length }
            : message
        )
      )

      if (index >= text.length && typingTimerRef.current) {
        window.clearInterval(typingTimerRef.current)
        typingTimerRef.current = null
      }
    }, 16)
  }

  const sendMessage = async (question: string) => {
    if (!question.trim()) return
    if (providerNeedsTest && connectionState !== 'ready') {
      setConnectionMessage('Test the provider connection before chatting.')
      return
    }

    setMessages((prev) => [...prev, { id: Date.now(), role: 'user', content: question }])
    setInput('')

    try {
      const response = await chatMutation.mutateAsync({
        topicId,
        question,
        providerConfig: config,
        history: messages,
      })
      animateAssistantReply(response.answer || 'No response')
    } catch (error) {
      const message = getErrorMessage(error, 'Sorry, I encountered an error. Please try again.')
      setMessages((prev) => [...prev, { id: Date.now(), role: 'ai', content: message }])
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    sendMessage(input)
  }

  return (
    <div className="flex h-full flex-col bg-[var(--bg)]">
      <div className="border-b border-[var(--border)] px-4 py-4 sm:px-5">
        <div className="flex items-start justify-between gap-3">
          <div className="min-w-0">
            <div className="flex items-center gap-2">
              <Sparkles className="h-4 w-4 text-[var(--accent)]" />
              <h3 className="text-sm font-medium text-[var(--fg)]">AI Assistant</h3>
            </div>
            <p className="mt-1 font-[var(--font-mono)] text-[0.625rem] uppercase tracking-[0.1em] text-[var(--muted)]" style={{ fontFamily: 'var(--font-mono)' }}>
              {topicName || 'General Study Mode'}
            </p>
          </div>
          <div className={`flex items-center gap-2 border px-3 py-2 text-[0.625rem] uppercase tracking-[0.12em] ${connectionState === 'ready' ? 'border-emerald-500/30 text-emerald-600' : connectionState === 'error' ? 'border-red-500/30 text-red-500' : 'border-[var(--border)] text-[var(--muted)]'}`}>
            {connectionState === 'ready' ? <ShieldCheck className="h-3.5 w-3.5" /> : connectionState === 'testing' ? <PlugZap className="h-3.5 w-3.5 animate-pulse" /> : <AlertTriangle className="h-3.5 w-3.5" />}
            {providerLabel}
          </div>
        </div>

        {showSettings ? (
          <div className="mt-4 grid gap-3 rounded-none border border-[var(--border)] bg-[var(--surface)] p-3 sm:grid-cols-[1.1fr_1fr_1fr]">
            <label className="space-y-1 text-xs text-[var(--muted)]">
              <span className="font-[var(--font-mono)] uppercase tracking-[0.1em]" style={{ fontFamily: 'var(--font-mono)' }}>Provider</span>
              <select
                value={config.provider}
                onChange={(e) => handleProviderChange(e.target.value as AIProvider)}
                className="w-full border border-[var(--border)] bg-[var(--bg)] px-3 py-2 text-sm text-[var(--fg)] outline-none focus:border-[var(--accent)]"
              >
                {providerOptions.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </label>

            {providerNeedsTest ? (
              <label className="space-y-1 text-xs text-[var(--muted)]">
                <span className="font-[var(--font-mono)] uppercase tracking-[0.1em]" style={{ fontFamily: 'var(--font-mono)' }}>Base URL</span>
                <input
                  type="text"
                  value={config.baseUrl || ''}
                  onChange={(e) => updateConfig({ baseUrl: e.target.value })}
                  placeholder={config.provider === 'anthropic' ? 'https://api.anthropic.com/v1' : 'https://api.openai.com/v1'}
                  className="w-full border border-[var(--border)] bg-[var(--bg)] px-3 py-2 text-sm text-[var(--fg)] outline-none focus:border-[var(--accent)]"
                />
              </label>
            ) : (
              <div className="space-y-1 text-xs text-[var(--muted)]">
                <span className="font-[var(--font-mono)] uppercase tracking-[0.1em]" style={{ fontFamily: 'var(--font-mono)' }}>Connection</span>
                <div className="border border-[var(--border)] px-3 py-2 text-sm text-[var(--fg)]">Uses backend local LLM</div>
              </div>
            )}

            {providerNeedsTest ? (
              <label className="space-y-1 text-xs text-[var(--muted)]">
                <span className="font-[var(--font-mono)] uppercase tracking-[0.1em]" style={{ fontFamily: 'var(--font-mono)' }}>API Key</span>
                <input
                  type="password"
                  value={config.apiKey || ''}
                  onChange={(e) => updateConfig({ apiKey: e.target.value })}
                  placeholder="sk-..."
                  className="w-full border border-[var(--border)] bg-[var(--bg)] px-3 py-2 text-sm text-[var(--fg)] outline-none focus:border-[var(--accent)]"
                />
              </label>
            ) : (
              <div className="space-y-1 text-xs text-[var(--muted)]">
                <span className="font-[var(--font-mono)] uppercase tracking-[0.1em]" style={{ fontFamily: 'var(--font-mono)' }}>Model</span>
                <div className="border border-[var(--border)] px-3 py-2 text-sm text-[var(--fg)]">Configured on backend</div>
              </div>
            )}

            {providerNeedsTest && (
              <label className="space-y-1 text-xs text-[var(--muted)] sm:col-span-2">
                <span className="font-[var(--font-mono)] uppercase tracking-[0.1em]" style={{ fontFamily: 'var(--font-mono)' }}>Model</span>
                <input
                  type="text"
                  value={config.model || ''}
                  onChange={(e) => updateConfig({ model: e.target.value })}
                  placeholder={config.provider === 'anthropic' ? 'claude-3-5-sonnet-latest' : config.provider === 'mimo' ? 'mimo-v2.5-pro' : 'gpt-4o-mini'}
                  className="w-full border border-[var(--border)] bg-[var(--bg)] px-3 py-2 text-sm text-[var(--fg)] outline-none focus:border-[var(--accent)]"
                />
              </label>
            )}

            <div className="flex items-end gap-2 sm:col-span-1">
              {providerNeedsTest ? (
                <button
                  type="button"
                  onClick={handleTestConnection}
                  disabled={testConnectionMutation.isPending || !config.baseUrl || !config.apiKey}
                  className="flex w-full items-center justify-center gap-2 border border-[var(--border)] px-3 py-2 text-sm text-[var(--fg)] transition-colors hover:border-[var(--accent)] hover:text-[var(--accent)] disabled:opacity-40"
                >
                  <PlugZap className="h-4 w-4" />
                  {testConnectionMutation.isPending ? 'Testing...' : 'Test connection'}
                </button>
              ) : (
                <div className="flex w-full items-center justify-center border border-[var(--border)] px-3 py-2 text-sm text-[var(--muted)]">Ready</div>
              )}
            </div>
          </div>
        ) : (
          <div className="mt-4 flex items-center justify-between gap-3 border border-[var(--border)] bg-[var(--surface)] px-3 py-3">
            <div className="min-w-0">
              <div className="flex items-center gap-2 text-sm text-[var(--fg)]">
                <ShieldCheck className="h-4 w-4 text-emerald-600" />
                <span>{providerLabel}</span>
                <span className="font-[var(--font-mono)] text-[0.625rem] uppercase tracking-[0.1em] text-emerald-600" style={{ fontFamily: 'var(--font-mono)' }}>
                  connected
                </span>
              </div>
              <p className="mt-1 text-xs text-[var(--muted)]">
                {connectionMessage || 'API is live and ready to chat.'}
              </p>
            </div>
            <button
              type="button"
              onClick={() => setShowSettings(true)}
              className="flex shrink-0 items-center gap-2 border border-[var(--border)] px-3 py-2 text-xs text-[var(--muted)] transition-colors hover:border-[var(--accent)] hover:text-[var(--accent)]"
            >
              Edit
            </button>
          </div>
        )}

        {connectionMessage && (
          <p className={`mt-3 text-xs ${connectionState === 'error' ? 'text-red-500' : connectionState === 'ready' ? 'text-emerald-600' : 'text-[var(--muted)]'}`}>
            {connectionMessage}
          </p>
        )}
      </div>

      <div className="flex-1 overflow-auto p-4 sm:p-5">
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

        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`mb-4 flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[85%] px-4 py-3 text-sm ${
                msg.role === 'user'
                  ? 'bg-[var(--accent)] text-[var(--bg)]'
                  : 'border border-[var(--border)] text-[var(--fg)]'
              }`}
            >
              {msg.role === 'ai' ? (
                msg.isTyping ? (
                  <p className="whitespace-pre-wrap leading-relaxed">
                    {msg.content}
                    <span className="ml-1 inline-block animate-pulse text-[var(--accent)]">▍</span>
                  </p>
                ) : (
                  <Markdown content={msg.content} className="text-[13px] leading-relaxed text-[var(--fg)] [&_p]:my-2 [&_li]:my-1 [&_strong]:font-semibold [&_code]:rounded [&_code]:bg-[var(--surface)] [&_code]:px-1.5 [&_code]:py-0.5 [&_code]:text-[12px] [&_pre]:overflow-x-auto [&_pre]:rounded-lg [&_pre]:bg-[var(--surface)] [&_pre]:p-4" />
                )
              ) : (
                <p className="whitespace-pre-wrap leading-relaxed">{msg.content}</p>
              )}
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

      <form onSubmit={handleSubmit} className="border-t border-[var(--border)] p-3 sm:p-4">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question..."
            disabled={providerNeedsTest && connectionState !== 'ready'}
            className="flex-1 border border-[var(--border)] bg-[var(--bg)] px-3 py-2 text-sm text-[var(--fg)] placeholder-[var(--muted)] outline-none transition-colors focus:border-[var(--accent)] disabled:opacity-40"
          />
          <button
            type="submit"
            disabled={chatMutation.isPending || !input.trim() || (providerNeedsTest && connectionState !== 'ready')}
            className="flex items-center justify-center bg-[var(--accent)] px-3 py-2 text-[var(--bg)] transition-opacity hover:opacity-90 disabled:opacity-40"
          >
            <Send className="h-4 w-4" />
          </button>
        </div>
      </form>
    </div>
  )
}
