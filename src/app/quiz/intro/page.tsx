"use client";

import Link from "next/link";
import { Suspense, useMemo } from "react";
import { useSearchParams } from "next/navigation";

import { QuizPageFallback, QuizPageShell } from "@/components/quiz/quiz-page-shell";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

function QuizIntroContent() {
  const searchParams = useSearchParams();
  const token = useMemo(() => searchParams.get("token") ?? "", [searchParams]);
  const quizId = useMemo(() => searchParams.get("quizId") ?? "", [searchParams]);

  return (
    <QuizPageShell>
      <Card className="border-primary/20">
        <CardHeader>
          <CardTitle className="text-2xl">开始前提示</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4 text-sm text-zinc-700">
          <p>1. 按直觉作答，结果会根据你的选择计算。</p>
          <p>2. 支持分支题与结果类型映射，提交后可查看历史。</p>
          <Link href={`/quiz/play?token=${token}&quizId=${quizId}`}>
            <Button className="w-full">开始答题</Button>
          </Link>
        </CardContent>
      </Card>
    </QuizPageShell>
  );
}

export default function QuizIntroPage() {
  return (
    <Suspense fallback={<QuizPageFallback text="页面加载中..." />}>
      <QuizIntroContent />
    </Suspense>
  );
}
