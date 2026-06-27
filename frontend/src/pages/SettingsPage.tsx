import { useState, useEffect } from 'react'
import { Settings, Sun, Moon, Activity, CheckCircle, XCircle } from 'lucide-react'
import { useHealthCheck } from '@/hooks/use-api'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'

export default function SettingsPage() {
  const [theme, setTheme] = useState<'dark' | 'light'>('light')
  const { data: health, isLoading, error } = useHealthCheck()

  useEffect(() => {
    document.documentElement.classList.toggle('dark', theme === 'dark')
  }, [theme])

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <div>
        <h1 className="flex items-center gap-3 text-2xl font-bold text-[#1a1a1a]">
          <Settings className="h-6 w-6 text-[#6b7280]" />
          Settings
        </h1>
        <p className="mt-1 text-sm text-[#6b7280]">
          Configure your preferences
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Appearance</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-[#1a1a1a]">Theme</p>
              <p className="text-xs text-[#9ca3af]">Toggle between dark and light mode</p>
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
            >
              {theme === 'dark' ? (
                <Sun className="mr-2 h-4 w-4" />
              ) : (
                <Moon className="mr-2 h-4 w-4" />
              )}
              {theme === 'dark' ? 'Light Mode' : 'Dark Mode'}
            </Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">API Status</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Activity className="h-4 w-4 text-[#6b7280]" />
              <div>
                <p className="text-sm font-medium text-[#1a1a1a]">Backend Connection</p>
                <p className="text-xs text-[#9ca3af]">http://localhost:8000</p>
              </div>
            </div>
            {isLoading ? (
              <Badge variant="outline">Checking...</Badge>
            ) : error ? (
              <div className="flex items-center gap-2">
                <XCircle className="h-4 w-4 text-[#ef4444]" />
                <Badge variant="destructive">Disconnected</Badge>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <CheckCircle className="h-4 w-4 text-[#10b981]" />
                <Badge variant="success">Connected</Badge>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">About</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-1 text-sm text-[#6b7280]">
            <p>KnowledgeNest AI - Smart Academic Platform</p>
            <p className="text-xs text-[#9ca3af]">Version 1.0.0</p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
