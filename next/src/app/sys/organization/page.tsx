"use client";

import { AdminShell } from "@/components/admin/admin-shell";
import { EntityPanel } from "@/components/admin/entity-panel";

export default function SysOrganizationPage() {
  return (
    <AdminShell>
      <EntityPanel
        title="组织管理"
        pageApi="/api/organization/tree"
        createApi="/api/organization/edit"
        createPayload={() => ({ enabled: true, seq: 0 })}
        columns={[
          { key: "name", label: "名称" },
          { key: "seq", label: "序号" },
          { key: "enabled", label: "启用" },
        ]}
      />
    </AdminShell>
  );
}
