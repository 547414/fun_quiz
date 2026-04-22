"use client";

import { AdminShell } from "@/components/admin/admin-shell";
import { EntityPanel } from "@/components/admin/entity-panel";

export default function SysMenuPage() {
  return (
    <AdminShell>
      <EntityPanel
        title="菜单管理"
        pageApi="/api/menu/page"
        createApi="/api/menu/edit"
        createPayload={() => ({ enabled: true, seq: 0 })}
        columns={[
          { key: "name", label: "名称" },
          { key: "code", label: "编码" },
          { key: "path", label: "路径" },
          { key: "enabled", label: "启用" },
        ]}
      />
    </AdminShell>
  );
}
