"use client";

import { useEffect, useState } from "react";

import { AdminShell } from "@/components/admin/admin-shell";
import { DataListPanel } from "@/components/admin/data-list-panel";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { TableCell, TableRow } from "@/components/ui/table";
import { postJson } from "@/lib/client-api";

type TokenItem = {
  id: string;
  token: string;
  status: string;
  maxUses: number;
  usedCount: number;
};

export default function QuizTokensPage() {
  const [list, setList] = useState<TokenItem[]>([]);
  const [quizIdsText, setQuizIdsText] = useState("");
  const [count, setCount] = useState("1");

  async function load() {
    const data = await postJson<{ list: TokenItem[] }>("/api/quiz_token/page", { pageIndex: 1, pageSize: 50 });
    setList(data.list);
  }

  useEffect(() => {
    void load();
  }, []);

  return (
    <AdminShell>
      <DataListPanel
        title="Token 管理"
        actions={
          <Button
            onClick={async () => {
              await postJson("/api/quiz_token/generate", {
                count: Number(count || "1"),
                maxUses: 1,
                quizIds: quizIdsText
                  .split(",")
                  .map((item) => item.trim())
                  .filter(Boolean),
              });
              await load();
            }}
          >
            生成 Token
          </Button>
        }
        filters={
          <div className="grid gap-3 sm:grid-cols-2">
            <Input placeholder="授权测验ID，逗号分隔" value={quizIdsText} onChange={(event) => setQuizIdsText(event.target.value)} />
            <Input placeholder="生成数量" value={count} onChange={(event) => setCount(event.target.value)} />
          </div>
        }
        headers={["Token", "状态", "最大次数", "已使用", "链接"]}
      >
        {list.map((item) => (
          <TableRow key={item.id}>
            <TableCell className="max-w-[260px] truncate">{item.token}</TableCell>
            <TableCell>
              <Badge variant={item.status === "active" ? "success" : item.status === "expired" ? "warning" : "outline"}>
                {item.status}
              </Badge>
            </TableCell>
            <TableCell>{item.maxUses}</TableCell>
            <TableCell>{item.usedCount}</TableCell>
            <TableCell>
              <a href={`/quiz?token=${item.token}`} target="_blank" rel="noreferrer">
                <Button size="sm" variant="surface">
                  打开答题页
                </Button>
              </a>
            </TableCell>
          </TableRow>
        ))}
      </DataListPanel>
    </AdminShell>
  );
}
