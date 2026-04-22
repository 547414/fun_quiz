import Link from "next/link";

export default function Home() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 p-8">
      <main className="w-full max-w-2xl rounded-2xl border border-zinc-200 bg-white p-10 shadow-sm">
        <h1 className="text-2xl font-semibold text-zinc-900">Fun Quiz Next 全栈复刻</h1>
        <p className="mt-2 text-zinc-600">功能对齐原系统，视觉采用全新设计语言。</p>
        <div className="mt-6 grid gap-3 sm:grid-cols-2">
          <Link href="/login" className="rounded-md border border-zinc-200 px-4 py-3 text-sm hover:bg-zinc-50">
            管理端登录
          </Link>
          <Link href="/quiz?token=demo" className="rounded-md border border-zinc-200 px-4 py-3 text-sm hover:bg-zinc-50">
            答题端入口
          </Link>
          <Link href="/quiz/list" className="rounded-md border border-zinc-200 px-4 py-3 text-sm hover:bg-zinc-50">
            测验管理
          </Link>
          <Link href="/sys/role" className="rounded-md border border-zinc-200 px-4 py-3 text-sm hover:bg-zinc-50">
            系统管理
          </Link>
        </div>
      </main>
    </div>
  );
}
