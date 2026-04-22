"use client";

import { AdminShell } from "@/components/admin/admin-shell";
import { EntityPanel } from "@/components/admin/entity-panel";

export default function SysInvitePage() {
  return (
    <AdminShell>
      <EntityPanel
        title="邀请码管理"
        pageApi="/api/invite_code/page"
        createApi="/api/invite_code/edit"
        createPayload={() => ({ enabled: true, maxUseTimes: 1 })}
        columns={[
          { key: "code", label: "邀请码" },
          { key: "enabled", label: "启用" },
          { key: "maxUseTimes", label: "总次数" },
          { key: "usedTimes", label: "已使用" },
        ]}
      />
    </AdminShell>
  );
}
