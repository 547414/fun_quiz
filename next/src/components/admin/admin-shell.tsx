"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { type ReactNode, useState } from "react";

import { Button } from "@/components/ui/button";
import { postJson } from "@/lib/client-api";
import { cn } from "@/lib/utils";

const navItems = [
  { href: "/quiz/list", label: "测验管理" },
  { href: "/quiz/tokens", label: "Token 管理" },
  { href: "/sys/people", label: "人员" },
  { href: "/sys/role", label: "角色" },
  { href: "/sys/menu", label: "菜单" },
  { href: "/sys/permission", label: "权限" },
  { href: "/sys/organization", label: "组织" },
  { href: "/sys/dept", label: "部门" },
  { href: "/sys/invite", label: "邀请码" },
];

export function AdminShell({ children }: { children: ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const [loggingOut, setLoggingOut] = useState(false);

  async function handleLogout() {
    try {
      setLoggingOut(true);
      await postJson("/api/union_user/logout");
    } finally {
      setLoggingOut(false);
      router.push("/login");
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-violet-50 to-cyan-50">
      <div className="mx-auto flex w-full max-w-[1400px] gap-4 p-4">
        <aside className="elevation-raised sticky top-4 flex h-[calc(100vh-2rem)] w-64 flex-col overflow-auto rounded-2xl border border-border bg-surface p-3">
          <div className="px-2 pb-3 text-sm font-semibold text-foreground">Fun Quiz Admin</div>
          <nav className="flex-1 space-y-1">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "block rounded-xl px-3 py-2 text-sm font-medium text-zinc-700 transition-all duration-200 hover:bg-primary/10 hover:text-primary",
                  pathname.startsWith(item.href) &&
                    "elevation-surface bg-gradient-to-r from-primary to-fuchsia-500 text-primary-foreground hover:bg-primary hover:text-primary-foreground",
                )}
              >
                {item.label}
              </Link>
            ))}
          </nav>
          <div className="mt-3 border-t border-border pt-3">
            <Button variant="surface" className="w-full" onClick={handleLogout} disabled={loggingOut}>
              {loggingOut ? "退出中..." : "退出登录"}
            </Button>
          </div>
        </aside>
        <main className="elevation-raised min-h-[calc(100vh-2rem)] flex-1 rounded-2xl border border-border bg-surface p-6">
          {children}
        </main>
      </div>
    </div>
  );
}
