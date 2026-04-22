"use client";

import { AdminShell } from "@/components/admin/admin-shell";
import { EntityPanel } from "@/components/admin/entity-panel";

export default function SysPermissionPage() {
  return (
    <AdminShell>
      <EntityPanel
        title="权限管理"
        pageApi="/api/permission/page"
        createApi="/api/permission/edit"
        createPayload={() => ({ enabled: true })}
        columns={[
          { key: "name", label: "名称" },
          { key: "code", label: "编码" },
          { key: "menuId", label: "菜单ID" },
          { key: "enabled", label: "启用" },
        ]}
      />
    </AdminShell>
  );
}
