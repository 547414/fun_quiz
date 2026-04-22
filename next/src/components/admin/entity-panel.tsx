"use client";

import { useCallback, useEffect, useState } from "react";

import { DataListPanel } from "@/components/admin/data-list-panel";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { TableCell, TableRow } from "@/components/ui/table";
import { postJson } from "@/lib/client-api";

type EntityPanelProps = {
  title: string;
  pageApi: string;
  createApi: string;
  createPayload: () => Record<string, unknown>;
  columns: Array<{ key: string; label: string }>;
};

export function EntityPanel({ title, pageApi, createApi, createPayload, columns }: EntityPanelProps) {
  const [list, setList] = useState<Array<Record<string, unknown>>>([]);
  const [name, setName] = useState("");
  const [code, setCode] = useState("");

  const load = useCallback(async () => {
    const data = await postJson<{ list: Array<Record<string, unknown>> }>(pageApi);
    setList(data.list);
  }, [pageApi]);

  useEffect(() => {
    void load();
  }, [load]);

  return (
    <div className="space-y-4">
      <DataListPanel
        title={title}
        actions={
          <Button
            onClick={async () => {
              const payload = createPayload();
              payload.name = name || payload.name || "新建项";
              payload.code = code || payload.code || `code_${Date.now()}`;
              await postJson(createApi, payload);
              setName("");
              setCode("");
              await load();
            }}
          >
            新建
          </Button>
        }
        filters={
          <div className="grid gap-3 sm:grid-cols-2">
            <Input placeholder="名称" value={name} onChange={(event) => setName(event.target.value)} />
            <Input placeholder="编码（可选）" value={code} onChange={(event) => setCode(event.target.value)} />
          </div>
        }
        headers={columns.map((column) => column.label)}
      >
        {list.map((item, index) => (
          <TableRow key={`${item.id ?? "row"}_${index}`}>
            {columns.map((column) => (
              <TableCell key={`${column.key}_${index}`}>{String(item[column.key] ?? "-")}</TableCell>
            ))}
          </TableRow>
        ))}
      </DataListPanel>
    </div>
  );
}
