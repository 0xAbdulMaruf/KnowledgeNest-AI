import { forwardRef, type HTMLAttributes } from 'react'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const badgeVariants = cva(
  'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium transition-colors',
  {
    variants: {
      variant: {
        default: 'bg-[var(--accent)]/10 text-[var(--accent)] border border-[var(--accent)]/20',
        secondary: 'bg-[var(--surface)] text-[var(--muted)] border border-[var(--border)]',
        outline: 'border border-[var(--border)] text-[var(--muted)]',
        success: 'bg-emerald-500/10 text-emerald-600 border border-emerald-500/20',
        warning: 'bg-amber-500/10 text-amber-600 border border-amber-500/20',
        accent: 'bg-[var(--accent)]/10 text-[var(--accent)] border border-[var(--accent)]/20',
        destructive: 'bg-red-500/10 text-red-500 border border-red-500/20',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
)

export interface BadgeProps
  extends HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

const Badge = forwardRef<HTMLDivElement, BadgeProps>(
  ({ className, variant, ...props }, ref) => {
    return (
      <div ref={ref} className={cn(badgeVariants({ variant }), className)} {...props} />
    )
  }
)
Badge.displayName = 'Badge'

export { Badge, badgeVariants }
