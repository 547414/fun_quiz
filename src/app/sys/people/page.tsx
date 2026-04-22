"use client";

import { useEffect, useState } from "react";

import { AdminShell } from "@/components/admin/admin-shell";
import { DataListPanel } from "@/components/admin/data-list-panel";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { TableCell, TableRow } from "@/components/ui/table";
import { postJson } from "@/lib/client-api";

type UserItem = {
  id: string;
  account: string;
  name: string;
  enabled: boolean;
};

export default function SysPeoplePage() {
  const [list, setList] = useState<UserItem[]>([]);
  const [account, setAccount] = useState("");
  const [name, setName] = useState("");

  async function load() {
    const data = await postJson<{ list: UserItem[] }>("/api/web_user/page");
    setList(data.list);
  }

  useEffect(() => {
    void load();
  }, []);

  return (
    <AdminShell>
      <div className="space-y-4">
        <DataListPanel
          title="人员管理"
          actions={
            <Button
              onClick={async () => {
                await postJson("/api/web_user/add", {
                  account,
                  name,
                  password: "123456",
                });
                setAccount("");
                setName("");
                await load();
              }}
            >
              新增人员
            </Button>
          }
          filters={
            <div className="grid gap-3 sm:grid-cols-2">
              <Input placeholder="账号" value={account} onChange={(event) => setAccount(event.target.value)} />
              <Input placeholder="姓名" value={name} onChange={(event) => setName(event.target.value)} />
            </div>
          }
          headers={["账号", "姓名", "启用"]}
        >
          {list.map((item) => (
            <TableRow key={item.id}>
              <TableCell>{item.account}</TableCell>
              <TableCell>{item.name}</TableCell>
              <TableCell>{String(item.enabled)}</TableCell>
            </TableRow>
          ))}
        </DataListPanel>
      </div>
    </AdminShell>
  );
}
