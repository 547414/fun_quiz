"use client";

import Link from "next/link";
import { Suspense, useEffect, useMemo, useState } from "react";
import { useSearchParams } from "next/navigation";

import { QuizPageFallback, QuizPageShell } from "@/components/quiz/quiz-page-shell";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import {
  List,
  ListEmpty,
  ListItem,
  ListItemActions,
  ListItemDescription,
  ListItemMeta,
  ListItemTitle,
} from "@/components/ui/list";
import { postJson } from "@/lib/client-api";

type EntryQuiz = {
  id: string;
  name: string;
  description: string;
};

type HistoryItem = {
  id: string;
  outcomeCode?: string;
  score?: number;
  createdAt: string;
};

type EntryMeta = {
  status: string;
  maxUses?: number | null;
  usedCount?: number;
};

function QuizEntryContent() {
  const searchParams = useSearchParams();
  const token = useMemo(() => searchParams.get("token") ?? "", [searchParams]);
  const [quizList, setQuizList] = useState<EntryQuiz[]>([]);
  const [historyList, setHistoryList] = useState<HistoryItem[]>([]);
  const [entryMeta, setEntryMeta] = useState<EntryMeta | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!token) {
      setEntryMeta(null);
      setQuizList([]);
      setHistoryList([]);
      return;
    }

    let cancelled = false;
    async function loadEntryData() {
      setError("");
      try {
        const meta = await postJson<EntryMeta>("/api/quiz_play/entry", { token });
        if (!cancelled) {
          setEntryMeta(meta);
        }
      } catch (entryError) {
        if (!cancelled) {
          setEntryMeta(null);
          setQuizList([]);
          setHistoryList([]);
          setError(entryError instanceof Error ? entryError.message : "Token 校验失败");
        }
        return;
      }

      postJson<{ list: EntryQuiz[] }>("/api/quiz_play/entry/quizzes", { token, pageIndex: 1, pageSize: 20 })
        .then((res) => {
          if (!cancelled) {
            setQuizList(res.list);
          }
        })
        .catch((entryError) => {
          if (!cancelled) {
            setError(entryError instanceof Error ? entryError.message : "测验列表加载失败");
          }
        });

      postJson<{ list: HistoryItem[] }>("/api/quiz_play/entry/history", { token, pageIndex: 1, pageSize: 10 })
        .then((res) => {
          if (!cancelled) {
            setHistoryList(res.list);
          }
        })
        .catch(() => {
          if (!cancelled) {
            setHistoryList([]);
          }
        });
    }

    void loadEntryData();
    return () => {
      cancelled = true;
    };
  }, [token]);

  const tokenStatusText = entryMeta
    ? entryMeta.status === "active"
      ? "可用"
      : entryMeta.status === "expired"
        ? "已过期"
        : entryMeta.status === "exhausted"
          ? "已用尽"
          : entryMeta.status
    : "-";

  return (
    <QuizPageShell vibrant>
      <Card className="border-primary/20">
        <CardHeader>
          <CardTitle className="text-2xl">趣味测验</CardTitle>
          <CardDescription>请选择一个测验开始体验</CardDescription>
        </CardHeader>
        <CardContent>
          {!token ? <p className="text-sm text-danger">缺少 token 参数</p> : null}
          {error ? <p className="text-sm text-danger">{error}</p> : null}
          {entryMeta ? (
            <p className="mb-3 text-xs text-zinc-600">
              Token 状态：{tokenStatusText}，已使用 {entryMeta.usedCount ?? 0} / {entryMeta.maxUses ?? "不限"}
            </p>
          ) : null}
          <List>
            {quizList.map((quiz) => (
              <ListItem key={quiz.id}>
                <ListItemTitle>{quiz.name}</ListItemTitle>
                <ListItemDescription>{quiz.description}</ListItemDescription>
                <ListItemActions>
                  <Link href={`/quiz/intro?token=${token}&quizId=${quiz.id}`}>
                    <Button size="sm">开始测验</Button>
                  </Link>
                </ListItemActions>
              </ListItem>
            ))}
            {!quizList.length ? (
              <ListEmpty>
                当前没有可用测验（请检查：测验是否已发布、token 是否绑定了正确的测验 ID）
              </ListEmpty>
            ) : null}
          </List>
          <div className="mt-6 border-t border-border pt-4">
            <p className="mb-2 text-sm font-semibold text-zinc-700">历史记录</p>
            <List className="space-y-2">
              {historyList.map((history) => (
                <ListItem key={history.id} className="p-3">
                  <Link href={`/quiz/result?token=${token}&resultId=${history.id}`} className="block">
                    <ListItemTitle className="text-sm">
                      {history.outcomeCode ?? "未命名结果"} · 分数 {history.score ?? 0}
                    </ListItemTitle>
                    <ListItemMeta className="mt-1">结果时间：{history.createdAt || "-"}</ListItemMeta>
                  </Link>
                </ListItem>
              ))}
              {!historyList.length ? <ListEmpty className="py-3 text-xs">暂无历史结果</ListEmpty> : null}
            </List>
          </div>
        </CardContent>
      </Card>
    </QuizPageShell>
  );
}

export default function QuizEntryPage() {
  return (
    <Suspense fallback={<QuizPageFallback text="入口加载中..." />}>
      <QuizEntryContent />
    </Suspense>
  );
}
