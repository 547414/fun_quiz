"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { postJson } from "@/lib/client-api";

export default function RegisterPage() {
  const router = useRouter();
  const [account, setAccount] = useState("");
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [inviteCode, setInviteCode] = useState("");
  const [error, setError] = useState("");

  const onSubmit = async () => {
    try {
      setError("");
      await postJson("/api/web_user/register", { account, name, password, inviteCode });
      router.push("/login");
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : "注册失败");
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-100 p-6">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>注册账号</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <Input placeholder="账号" value={account} onChange={(event) => setAccount(event.target.value)} />
          <Input placeholder="姓名" value={name} onChange={(event) => setName(event.target.value)} />
          <Input type="password" placeholder="密码" value={password} onChange={(event) => setPassword(event.target.value)} />
          <Input placeholder="邀请码" value={inviteCode} onChange={(event) => setInviteCode(event.target.value)} />
          {error ? <p className="text-sm text-red-500">{error}</p> : null}
          <Button className="w-full" onClick={onSubmit}>
            注册
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
