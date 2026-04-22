"use client";

import Link from "next/link";
import { Suspense, useEffect, useMemo, useState } from "react";
import { useSearchParams } from "next/navigation";

import { QuizPageFallback, QuizPageShell } from "@/components/quiz/quiz-page-shell";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { postJson } from "@/lib/client-api";

type ResultData = {
  outcomeName?: string | null;
  outcomeCode?: string | null;
  score: number;
};

function QuizResultContent() {
  const searchParams = useSearchParams();
  const token = useMemo(() => searchParams.get("token") ?? "", [searchParams]);
  const resultId = useMemo(() => searchParams.get("resultId") ?? "", [searchParams]);
  const [result, setResult] = useState<ResultData | null>(null);

  useEffect(() => {
    if (!resultId || !token) return;
    postJson<ResultData>("/api/quiz_play/result", { token, resultId }).then(setResult);
  }, [resultId, token]);

  return (
    <QuizPageShell vibrant>
      <Card className="border-primary/20">
        <CardHeader>
          <CardTitle className="text-2xl">测验结果</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-sm text-zinc-500">结果ID：{resultId}</p>
          <p className="text-xl font-semibold text-foreground">{result?.outcomeName ?? "正在计算..."}</p>
          <div className="flex items-center gap-2">
            <Badge variant="info">结果编码：{result?.outcomeCode ?? "-"}</Badge>
            <Badge variant="success">得分：{result?.score ?? 0}</Badge>
          </div>
          <div className="flex gap-2">
            <Link href={`/quiz?token=${token}`}>
              <Button variant="surface">返回列表</Button>
            </Link>
            <Button
              onClick={async () => {
                if (navigator.share) {
                  await navigator.share({
                    title: "我的测验结果",
                    text: `结果：${result?.outcomeName ?? ""}`,
                    url: window.location.href,
                  });
                  return;
                }
                await navigator.clipboard.writeText(window.location.href);
              }}
            >
              分享结果
            </Button>
          </div>
        </CardContent>
      </Card>
    </QuizPageShell>
  );
}

export default function QuizResultPage() {
  return (
    <Suspense fallback={<QuizPageFallback text="结果页加载中..." />}>
      <QuizResultContent />
    </Suspense>
  );
}
