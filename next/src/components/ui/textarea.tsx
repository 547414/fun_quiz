import * as React from "react";

import { cn } from "@/lib/utils";

export type TextareaProps = React.TextareaHTMLAttributes<HTMLTextAreaElement>;

export function Textarea({ className, ...props }: TextareaProps) {
  return (
    <textarea
      className={cn(
        "min-h-[96px] w-full rounded-xl border border-border bg-surface px-3 py-2 text-sm text-foreground placeholder:text-zinc-400 shadow-[var(--shadow-surface)] transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/45 focus-visible:ring-offset-2 focus-visible:ring-offset-background",
        className,
      )}
      {...props}
    />
  );
}
