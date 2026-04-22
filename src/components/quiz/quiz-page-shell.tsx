import type { ReactNode } from "react";

import { cn } from "@/lib/utils";

type QuizPageShellProps = {
  children: ReactNode;
  maxWidthClassName?: string;
  className?: string;
  vibrant?: boolean;
};

export function QuizPageShell({
  children,
  maxWidthClassName = "max-w-xl",
  className,
  vibrant = false,
}: QuizPageShellProps) {
  return (
    <div
      className={cn(
        "min-h-screen p-4",
        vibrant
          ? "bg-gradient-to-br from-indigo-100 via-violet-50 to-cyan-100"
          : "bg-gradient-to-b from-indigo-50 to-surface-muted",
        className,
      )}
    >
      <div className={cn("mx-auto space-y-4", maxWidthClassName)}>{children}</div>
    </div>
  );
}

export function QuizPageFallback({ text }: { text: string }) {
  return <div className="p-4 text-sm text-zinc-600">{text}</div>;
}
