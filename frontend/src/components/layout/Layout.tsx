import { Outlet } from 'react-router-dom'
import Header from './Header'
import AIAssistantLauncher from '@/components/ai/AIAssistantLauncher'

export default function Layout() {
  return (
    <div className="min-h-screen flex flex-col" style={{ background: 'var(--bg)' }}>
      <Header />

      {/* Main content — pushed down 80px to clear the fixed header */}
      <main className="flex-1 w-full" style={{ paddingTop: '80px' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '32px 24px' }}>
          <Outlet />
        </div>
      </main>

      <AIAssistantLauncher />

      {/* Footer */}
      <footer
        className="w-full"
        style={{
          borderTop: '1px solid var(--border)',
          background: 'var(--bg)',
          padding: '48px 24px',
          marginTop: '80px',
        }}
      >
        <div style={{ maxWidth: '1200px', margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <img src="/logo.png" alt="KnowledgeNest AI Logo" style={{ height: '28px', width: '28px', objectFit: 'contain', opacity: 0.8 }} />
            <span style={{ fontFamily: 'var(--font-display)', fontSize: '14px', fontWeight: 600, color: 'var(--fg)' }}>
              KnowledgeNest AI
            </span>
          </div>
          <p style={{ fontSize: '12px', color: 'var(--muted)' }}>
            © {new Date().getFullYear()} KnowledgeNest AI. Safe & Smart Academic Platform.
          </p>
        </div>
      </footer>
    </div>
  )
}
