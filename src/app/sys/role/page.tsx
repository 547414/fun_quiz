"use client";

import { AdminShell } from "@/components/admin/admin-shell";
import { EntityPanel } from "@/components/admin/entity-panel";

export default function SysRolePage() {
  return (
    <AdminShell>
      <EntityPanel
        title="角色管理"
        pageApi="/api/role/page"
        createApi="/api/role/edit"
        createPayload={() => ({ enabled: true })}
        columns={[
          { key: "name", label: "名称" },
          { key: "code", label: "编码" },
          { key: "enabled", label: "启用" },
        ]}
      />
    </AdminShell>
  );
}
