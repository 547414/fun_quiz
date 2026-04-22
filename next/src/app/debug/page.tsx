"use client";

import { useState } from "react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { postJson } from "@/lib/client-api";

export default function DebugPage() {
  const [output, setOutput] = useState("");

  return (
    <div className="min-h-screen bg-zinc-100 p-4">
      <div className="mx-auto max-w-3xl space-y-4">
        <Card>
          <CardHeader>
            <CardTitle>调试面板</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <Button
              onClick={async () => {
                const data = await postJson("/api/quiz/page");
                setOutput(JSON.stringify(data, null, 2));
              }}
            >
              拉取测验列表
            </Button>
            <Textarea value={output} readOnly className="min-h-[420px] font-mono text-xs" />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
