import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";

import { cn } from "@/lib/utils";

const badgeVariants = cva(
  "inline-flex items-center rounded-full border px-2.5 py-1 text-xs font-semibold shadow-[var(--shadow-surface)]",
  {
  variants: {
    variant: {
      default: "border-transparent bg-primary/15 text-primary",
      outline: "border-border bg-surface text-foreground",
      success: "border-transparent bg-success/20 text-emerald-700",
      warning: "border-transparent bg-warning/20 text-amber-800",
      info: "border-transparent bg-info/20 text-blue-700",
      danger: "border-transparent bg-danger/20 text-red-700",
    },
  },
  defaultVariants: {
    variant: "default",
  },
});

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement>, VariantProps<typeof badgeVariants> {}

export function Badge({ className, variant, ...props }: BadgeProps) {
  return <div className={cn(badgeVariants({ variant }), className)} {...props} />;
}
