import { createContext, useContext, useState, type ReactNode } from 'react'
import { cn } from '@/lib/utils'

interface TabsContextValue {
  value: string
  onValueChange: (value: string) => void
}

const TabsContext = createContext<TabsContextValue>({
  value: '',
  onValueChange: () => {},
})

interface TabsProps {
  value?: string
  defaultValue?: string
  onValueChange?: (value: string) => void
  children: ReactNode
  className?: string
}

export function Tabs({ value: controlledValue, defaultValue, onValueChange, children, className }: TabsProps) {
  const [uncontrolledValue, setUncontrolledValue] = useState(defaultValue || '')
  const value = controlledValue ?? uncontrolledValue
  const handleValueChange = (v: string) => {
    setUncontrolledValue(v)
    onValueChange?.(v)
  }

  return (
    <TabsContext.Provider value={{ value, onValueChange: handleValueChange }}>
      <div className={className}>{children}</div>
    </TabsContext.Provider>
  )
}

interface TabsListProps {
  children: ReactNode
  className?: string
}

export function TabsList({ children, className }: TabsListProps) {
  return (
    <div className={cn('inline-flex items-center gap-1 border-b border-[#e5e7eb]', className)}>
      {children}
    </div>
  )
}

interface TabsTriggerProps {
  value: string
  children: ReactNode
  className?: string
}

export function TabsTrigger({ value, children, className }: TabsTriggerProps) {
  const ctx = useContext(TabsContext)
  const isActive = ctx.value === value

  return (
    <button
      className={cn(
        'inline-flex items-center justify-center whitespace-nowrap px-4 py-2.5 text-sm font-medium transition-all duration-150 border-b-2 -mb-px',
        isActive
          ? 'border-[#3b82f6] text-[#3b82f6]'
          : 'border-transparent text-[#6b7280] hover:text-[#1a1a1a] hover:border-[#e5e7eb]',
        className
      )}
      onClick={() => ctx.onValueChange(value)}
    >
      {children}
    </button>
  )
}

interface TabsContentProps {
  value: string
  children: ReactNode
  className?: string
}

export function TabsContent({ value, children, className }: TabsContentProps) {
  const ctx = useContext(TabsContext)
  if (ctx.value !== value) return null
  return <div className={cn('mt-6', className)}>{children}</div>
}
