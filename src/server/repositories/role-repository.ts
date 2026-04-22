import { eq } from "drizzle-orm";

import { db } from "@/db";
import { roles } from "@/db/schema/core";

export async function getAllRoles() {
  return db.select().from(roles);
}

export async function findRoleByCode(code: string) {
  const [row] = await db.select().from(roles).where(eq(roles.code, code)).limit(1);
  return row ?? null;
}

export async function upsertBuiltinRoles() {
  const builtin = [
    { id: "role_super_admin", name: "超级管理员", code: "SUPER_ADMIN", enabled: true, remark: "system" },
    { id: "role_admin", name: "管理员", code: "ADMIN", enabled: true, remark: "system" },
    { id: "role_web_user", name: "普通用户", code: "WEB_USER", enabled: true, remark: "system" },
  ] as const;

  for (const item of builtin) {
    const exists = await findRoleByCode(item.code);
    if (!exists) {
      await db.insert(roles).values(item);
    }
  }
}
