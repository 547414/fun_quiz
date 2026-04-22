"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { postJson } from "@/lib/client-api";

export default function LoginPage() {
  const router = useRouter();
  const [account, setAccount] = useState("admin");
  const [password, setPassword] = useState("admin123");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [bootstrapTip, setBootstrapTip] = useState("");

  const onSubmit = async () => {
    setLoading(true);
    setError("");
    try {
      await postJson("/api/web_user/login", {
        account,
        password,
        scene: "WEB",
        space: "WEB",
      });
      router.push("/quiz/list");
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : "登录失败");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-zinc-100 to-slate-200 p-6">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>管理端登录</CardTitle>
          <CardDescription>首次初始化后会返回一次性管理员密码，请及时妥善保存。</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <Input placeholder="账号" value={account} onChange={(event) => setAccount(event.target.value)} />
          <Input type="password" placeholder="密码" value={password} onChange={(event) => setPassword(event.target.value)} />
          {error ? <p className="text-sm text-red-600">{error}</p> : null}
          {bootstrapTip ? <p className="text-sm text-emerald-600">{bootstrapTip}</p> : null}
          <div className="flex gap-2">
            <Button className="flex-1" onClick={onSubmit} disabled={loading}>
              {loading ? "登录中..." : "登录"}
            </Button>
            <Button
              variant="outline"
              onClick={async () => {
                try {
                  setError("");
                  const result = await postJson<{ adminAccount: string; created: boolean; initialPassword?: string }>("/api/system/bootstrap");
                  setAccount(result.adminAccount);
                  if (result.initialPassword) {
                    setPassword(result.initialPassword);
                    setBootstrapTip("初始化成功：已填入一次性管理员密码，请立即登录并修改。");
                    return;
                  }
                  setBootstrapTip("系统已初始化，请使用已有管理员密码登录。");
                } catch (bootstrapError) {
                  setBootstrapTip("");
                  setError(bootstrapError instanceof Error ? bootstrapError.message : "初始化失败");
                }
              }}
            >
              初始化
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
