import * as React from "react";

import { cn } from "@/lib/utils";

export function List({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("space-y-3", className)} {...props} />;
}

export function ListItem({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn(
        "elevation-surface rounded-2xl border border-border/90 bg-surface p-4 transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[var(--shadow-raised)]",
        className,
      )}
      {...props}
    />
  );
}

export function ListItemHeader({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("flex items-start justify-between gap-3", className)} {...props} />;
}

export function ListItemTitle({ className, ...props }: React.HTMLAttributes<HTMLHeadingElement>) {
  return <h3 className={cn("font-semibold text-foreground", className)} {...props} />;
}

export function ListItemDescription({ className, ...props }: React.HTMLAttributes<HTMLParagraphElement>) {
  return <p className={cn("mt-1 text-sm text-zinc-600", className)} {...props} />;
}

export function ListItemMeta({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("text-xs text-zinc-500", className)} {...props} />;
}

export function ListItemActions({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("mt-3 flex items-center gap-2", className)} {...props} />;
}

export function ListEmpty({ className, ...props }: React.HTMLAttributes<HTMLParagraphElement>) {
  return (
    <p
      className={cn(
        "rounded-xl border border-dashed border-border bg-surface-muted px-3 py-4 text-center text-sm text-zinc-500",
        className,
      )}
      {...props}
    />
  );
}
