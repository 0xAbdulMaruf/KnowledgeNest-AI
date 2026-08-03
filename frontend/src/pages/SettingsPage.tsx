import { useEffect, useState } from 'react'
import { Activity, CheckCircle, Code2, KeyRound, Moon, RotateCcw, Settings, Sun, XCircle } from 'lucide-react'
import { useAIConfig, useHealthCheck, useTestAIConnection } from '@/hooks/use-api'
import { AI_DEVELOPER_CONFIG_KEY, unlockAIDeveloper } from '@/services/api'
import type { AIProvider, AIProviderConfig } from '@/services/api'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'

const developerDefaults: AIProviderConfig = { provider: 'local', baseUrl: '', apiKey: '', model: '' }
const providers: { value: AIProvider; label: string }[] = [
  { value: 'local', label: 'Local LLM' },
  { value: 'openai', label: 'OpenAI' },
  { value: 'anthropic', label: 'Anthropic' },
  { value: 'mimo', label: 'Mimo' },
]

function loadDeveloperConfig(): AIProviderConfig {
  try {
    const raw = sessionStorage.getItem(AI_DEVELOPER_CONFIG_KEY)
    if (!raw) return developerDefaults
    const parsed = JSON.parse(raw) as Partial<AIProviderConfig>
    return { ...developerDefaults, ...parsed, apiKey: parsed.apiKey || '' }
  } catch {
    return developerDefaults
  }
}

export default function SettingsPage() {
  const [theme, setTheme] = useState<'dark' | 'light'>('light')
  const [developerEnabled, setDeveloperEnabled] = useState(() => Boolean(sessionStorage.getItem(AI_DEVELOPER_CONFIG_KEY)))
  const [developerConfig, setDeveloperConfig] = useState<AIProviderConfig>(loadDeveloperConfig)
  const [developerPassword, setDeveloperPassword] = useState('')
  const [developerUnlocked, setDeveloperUnlocked] = useState(() => Boolean(loadDeveloperConfig().developerToken))
  const [developerError, setDeveloperError] = useState('')
  const [connectionMessage, setConnectionMessage] = useState('')
  const [saved, setSaved] = useState(false)
  const { data: health, isLoading, error } = useHealthCheck()
  const { data: aiConfig } = useAIConfig()
  const testConnection = useTestAIConnection()

  useEffect(() => {
    document.documentElement.classList.toggle('dark', theme === 'dark')
  }, [theme])

  const updateDeveloperConfig = (patch: Partial<AIProviderConfig>) => {
    setDeveloperConfig((current) => ({ ...current, ...patch }))
    setSaved(false)
  }

  const unlockDeveloper = async () => {
    setDeveloperError('')
    try {
      const response = await unlockAIDeveloper(developerPassword)
      const nextConfig = { ...developerConfig, developerToken: response.access_token }
      setDeveloperConfig(nextConfig)
      setDeveloperUnlocked(true)
      setDeveloperEnabled(true)
      setDeveloperPassword('')
    } catch {
      setDeveloperError('Invalid developer password or developer access is not configured.')
    }
  }

  const handleTestConnection = async () => {
    if (!developerUnlocked || !developerConfig.developerToken) return
    setConnectionMessage('Testing AI provider…')
    try {
      const result = await testConnection.mutateAsync(developerConfig)
      setConnectionMessage(result.message)
    } catch {
      setConnectionMessage('Connection test failed. Check the provider settings and try again.')
    }
  }

  const saveDeveloperConfig = () => {
    if (!developerEnabled || !developerUnlocked || !developerConfig.developerToken) {
      sessionStorage.removeItem(AI_DEVELOPER_CONFIG_KEY)
    } else {
      sessionStorage.setItem(AI_DEVELOPER_CONFIG_KEY, JSON.stringify(developerConfig))
    }
    window.dispatchEvent(new Event('kn-ai-developer-config-changed'))
    setSaved(true)
    window.setTimeout(() => setSaved(false), 2500)
  }

  const resetDeveloperConfig = () => {
    sessionStorage.removeItem(AI_DEVELOPER_CONFIG_KEY)
    setDeveloperConfig(developerDefaults)
    setDeveloperEnabled(false)
    setDeveloperUnlocked(false)
    setDeveloperError('')
    window.dispatchEvent(new Event('kn-ai-developer-config-changed'))
    setSaved(true)
    window.setTimeout(() => setSaved(false), 2500)
  }

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <div>
        <h1 className="flex items-center gap-3 text-2xl font-bold text-[var(--fg)]"><Settings className="h-6 w-6 text-[var(--muted)]" />Settings</h1>
        <p className="mt-1 text-sm text-[var(--muted)]">Configure your preferences</p>
      </div>

      <Card>
        <CardHeader><CardTitle className="text-base">Appearance</CardTitle></CardHeader>
        <CardContent>
          <div className="flex items-center justify-between">
            <div><p className="text-sm font-medium text-[var(--fg)]">Theme</p><p className="text-xs text-[var(--muted)]">Toggle between dark and light mode</p></div>
            <Button variant="outline" size="sm" onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}>
              {theme === 'dark' ? <Sun className="mr-2 h-4 w-4" /> : <Moon className="mr-2 h-4 w-4" />}{theme === 'dark' ? 'Light Mode' : 'Dark Mode'}
            </Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader><CardTitle className="flex items-center gap-2 text-base"><Code2 className="h-4 w-4 text-[var(--accent)]" />Developer Options</CardTitle></CardHeader>
        <CardContent className="space-y-5">
          <div className="border border-amber-500/30 bg-amber-500/5 p-3 text-xs leading-relaxed text-[var(--muted)]">
            Normal users cannot configure the AI from the chat. The server uses `.env` by default. Enable this only for local development; values are kept in this browser session and are cleared when the session ends.
          </div>
          {!aiConfig?.developer_options_enabled ? <p className="border-t border-[var(--border)] pt-4 text-xs text-[var(--muted)]">Developer options are disabled in the server configuration.</p> : !developerUnlocked ? <div className="space-y-3 border-t border-[var(--border)] pt-4"><label className="block text-xs text-[var(--muted)]"><span className="mb-1 block uppercase tracking-wider">Developer password</span><input type="password" value={developerPassword} onChange={(event) => setDeveloperPassword(event.target.value)} placeholder="Enter developer password" className="w-full border border-[var(--border)] bg-[var(--bg)] px-3 py-2 text-sm text-[var(--fg)]" /></label><Button size="sm" onClick={unlockDeveloper} disabled={!developerPassword}>Unlock developer options</Button>{developerError && <p className="text-xs text-red-500">{developerError}</p>}</div> : <><label className="flex items-center justify-between gap-4"><span><span className="block text-sm font-medium text-[var(--fg)]">Enable temporary override</span><span className="block text-xs text-[var(--muted)]">Use these values for the current browser session</span></span><input type="checkbox" checked={developerEnabled} onChange={(event) => { setDeveloperEnabled(event.target.checked); setSaved(false) }} className="h-4 w-4 accent-[var(--accent)]" /></label>{developerEnabled && <div className="space-y-4 border-t border-[var(--border)] pt-4">
            <label className="block text-xs text-[var(--muted)]"><span className="mb-1 block uppercase tracking-wider">Provider</span><select value={developerConfig.provider} onChange={(event) => updateDeveloperConfig({ provider: event.target.value as AIProvider })} className="w-full border border-[var(--border)] bg-[var(--bg)] px-3 py-2 text-sm text-[var(--fg)]"><>{providers.map((provider) => <option key={provider.value} value={provider.value}>{provider.label}</option>)}</></select></label>
            <label className="block text-xs text-[var(--muted)]"><span className="mb-1 block uppercase tracking-wider">Base URL</span><input value={developerConfig.baseUrl || ''} onChange={(event) => updateDeveloperConfig({ baseUrl: event.target.value })} placeholder="Leave empty to use server .env" className="w-full border border-[var(--border)] bg-[var(--bg)] px-3 py-2 text-sm text-[var(--fg)]" /></label>
            <label className="block text-xs text-[var(--muted)]"><span className="mb-1 block uppercase tracking-wider">Model</span><input value={developerConfig.model || ''} onChange={(event) => updateDeveloperConfig({ model: event.target.value })} placeholder="Leave empty to use server .env" className="w-full border border-[var(--border)] bg-[var(--bg)] px-3 py-2 text-sm text-[var(--fg)]" /></label>
            <label className="block text-xs text-[var(--muted)]"><span className="mb-1 flex items-center gap-1 uppercase tracking-wider"><KeyRound className="h-3 w-3" />API key</span><input type="password" value={developerConfig.apiKey || ''} onChange={(event) => updateDeveloperConfig({ apiKey: event.target.value })} placeholder="Session-only API key" className="w-full border border-[var(--border)] bg-[var(--bg)] px-3 py-2 text-sm text-[var(--fg)]" /></label>
          </div>}</>}
          <div className="flex flex-wrap gap-2"><Button size="sm" onClick={saveDeveloperConfig} disabled={!developerUnlocked}>{saved ? <CheckCircle className="mr-2 h-4 w-4" /> : null}{saved ? 'Saved' : 'Apply for this session'}</Button><Button variant="outline" size="sm" onClick={handleTestConnection} disabled={!developerUnlocked || testConnection.isPending}>{testConnection.isPending ? 'Testing…' : 'Test AI connection'}</Button><Button variant="outline" size="sm" onClick={resetDeveloperConfig}><RotateCcw className="mr-2 h-4 w-4" />Use server config</Button></div>
          {connectionMessage && <p className={`text-xs ${connectionMessage.includes('failed') ? 'text-red-500' : 'text-[var(--muted)]'}`}>{connectionMessage}</p>}
          <div className="border-t border-[var(--border)] pt-4 text-xs text-[var(--muted)]"><p>Server configuration</p><p className="mt-1">Provider: <strong className="text-[var(--fg)]">{aiConfig?.provider || '—'}</strong> · Model: <strong className="text-[var(--fg)]">{aiConfig?.model || 'default'}</strong> · API key: <strong className="text-[var(--fg)]">{aiConfig?.api_key_configured ? 'configured' : 'not configured'}</strong></p></div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader><CardTitle className="text-base">API Status</CardTitle></CardHeader>
        <CardContent><div className="flex items-center justify-between"><div className="flex items-center gap-3"><Activity className="h-4 w-4 text-[var(--muted)]" /><div><p className="text-sm font-medium text-[var(--fg)]">Backend Connection</p><p className="text-xs text-[var(--muted)]">{window.location.origin}</p></div></div>{isLoading ? <Badge variant="outline">Checking...</Badge> : error ? <div className="flex items-center gap-2"><XCircle className="h-4 w-4 text-red-500" /><Badge variant="destructive">Disconnected</Badge></div> : <div className="flex items-center gap-2"><CheckCircle className="h-4 w-4 text-emerald-500" /><Badge variant="success">Connected</Badge></div>}</div></CardContent>
      </Card>

      <Card><CardHeader><CardTitle className="text-base">About</CardTitle></CardHeader><CardContent><div className="space-y-1 text-sm text-[var(--muted)]"><p>KnowledgeNest AI - Smart Academic Platform</p><p className="text-xs text-[var(--muted)]">Version 1.0.0</p></div></CardContent></Card>
    </div>
  )
}
