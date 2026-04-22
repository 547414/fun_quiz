"use client";

import { AdminShell } from "@/components/admin/admin-shell";
import { EntityPanel } from "@/components/admin/entity-panel";

export default function SysDeptPage() {
  return (
    <AdminShell>
      <EntityPanel
        title="部门管理"
        pageApi="/api/dept/tree"
        createApi="/api/dept/edit"
        createPayload={() => ({ enabled: true, seq: 0 })}
        columns={[
          { key: "name", label: "名称" },
          { key: "organizationId", label: "组织ID" },
          { key: "enabled", label: "启用" },
        ]}
      />
    </AdminShell>
  );
}
