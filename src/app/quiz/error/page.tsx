import Link from "next/link";

import { QuizPageShell } from "@/components/quiz/quiz-page-shell";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function QuizErrorPage() {
  return (
    <QuizPageShell className="flex items-center justify-center">
      <Card className="w-full max-w-md border-danger/30">
        <CardHeader>
          <CardTitle className="text-danger">入口无效</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4 text-sm text-zinc-700">
          <p>当前测验链接无效或已过期，请联系管理员重新获取 Token。</p>
          <Link href="/">
            <Button variant="surface">返回首页</Button>
          </Link>
        </CardContent>
      </Card>
    </QuizPageShell>
  );
}
