import { forwardRef, type HTMLAttributes } from 'react'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const badgeVariants = cva(
  'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium transition-colors',
  {
    variants: {
      variant: {
        default: 'bg-[#3b82f6]/10 text-[#3b82f6] border border-[#3b82f6]/20',
        secondary: 'bg-[#f3f4f6] text-[#6b7280] border border-[#e5e7eb]',
        outline: 'border border-[#e5e7eb] text-[#6b7280]',
        success: 'bg-[#10b981]/10 text-[#10b981] border border-[#10b981]/20',
        warning: 'bg-[#f59e0b]/10 text-[#f59e0b] border border-[#f59e0b]/20',
        accent: 'bg-[#3b82f6]/10 text-[#3b82f6] border border-[#3b82f6]/20',
        destructive: 'bg-[#ef4444]/10 text-[#ef4444] border border-[#ef4444]/20',
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
