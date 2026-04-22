"use client";

import { Suspense, useEffect, useMemo, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";

import { QuizPageFallback, QuizPageShell } from "@/components/quiz/quiz-page-shell";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { postJson } from "@/lib/client-api";

type Question = {
  id: string;
  seq: number;
  content: string;
  options: Array<{ code?: string; key?: string; label?: string; nextQuestionSeq?: number; next_question_seq?: number; outcomeCode?: string }>;
};

function QuizPlayContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const token = useMemo(() => searchParams.get("token") ?? "", [searchParams]);
  const quizId = useMemo(() => searchParams.get("quizId") ?? "", [searchParams]);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [quizType, setQuizType] = useState<string>("score");
  const [index, setIndex] = useState(0);
  const [answers, setAnswers] = useState<Array<Record<string, unknown>>>([]);

  useEffect(() => {
    if (!token || !quizId) return;
    postJson<{ questions: Question[]; quiz: { quizType?: string } }>("/api/quiz_play/play", { token, quizId }).then((data) => {
      setQuestions(data.questions);
      setQuizType(data.quiz?.quizType ?? "score");
    });
  }, [token, quizId]);

  const current = questions[index];
  const seqIndexMap = useMemo(() => {
    const map = new Map<number, number>();
    questions.forEach((item, idx) => map.set(item.seq, idx));
    return map;
  }, [questions]);

  return (
    <QuizPageShell>
      <Card className="border-primary/20">
        <CardHeader>
          <CardTitle className="text-xl">
            第 {Math.min(index + 1, questions.length)} / {questions.length || 1} 题
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-base font-medium text-foreground">{current?.content ?? "题目加载中..."}</p>
          <div className="space-y-2">
            {(current?.options ?? []).map((option, optionIndex) => (
              <Button
                key={`${option.code ?? "option"}_${optionIndex}`}
                variant="surface"
                className="w-full justify-start"
                onClick={() => {
                  const nextAnswers = [
                    ...answers,
                    {
                      questionId: current.id,
                      questionSeq: current.seq,
                      optionCode: option.key ?? option.code ?? String(optionIndex + 1),
                    },
                  ];
                  const nextQuestionSeq = Number(option.nextQuestionSeq ?? option.next_question_seq ?? 0);
                  const isBranchEnd = quizType === "branch" && nextQuestionSeq === -1;
                  if (isBranchEnd || index >= questions.length - 1) {
                    postJson<{ resultId: string }>("/api/quiz_play/submit", {
                      token,
                      quizId,
                      answers: nextAnswers,
                    }).then((result) => {
                      router.push(`/quiz/result?token=${token}&resultId=${result.resultId}`);
                    });
                    return;
                  }
                  setAnswers(nextAnswers);
                  if (quizType === "branch" && nextQuestionSeq > 0 && seqIndexMap.has(nextQuestionSeq)) {
                    setIndex(seqIndexMap.get(nextQuestionSeq)!);
                  } else {
                    setIndex((prev) => prev + 1);
                  }
                }}
              >
                {option.label ?? option.key ?? option.code ?? `选项 ${optionIndex + 1}`}
              </Button>
            ))}
          </div>
        </CardContent>
      </Card>
    </QuizPageShell>
  );
}

export default function QuizPlayPage() {
  return (
    <Suspense fallback={<QuizPageFallback text="答题页加载中..." />}>
      <QuizPlayContent />
    </Suspense>
  );
}
