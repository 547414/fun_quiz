import { asc, eq, inArray } from "drizzle-orm";

import { db } from "@/db";
import { menus, permissionAssigns, permissions, userRoles } from "@/db/schema/core";
import { requireAuth } from "@/lib/auth/guard";
import { withApi } from "@/lib/http";

function buildTree(items: Array<typeof menus.$inferSelect>, parentId: string | null = null): Array<Record<string, unknown>> {
  return items
    .filter((item) => (item.parentId ?? null) === parentId)
    .map((item) => ({
      ...item,
      children: buildTree(items, item.id),
    }));
}

export async function POST() {
  return withApi(async () => {
    const current = await requireAuth();
    const roleRows = await db.select().from(userRoles).where(eq(userRoles.userId, current.webUserId));
    if (!roleRows.length) return [];

    const roleIds = roleRows.map((item) => item.roleId);
    const assignRows = await db.select().from(permissionAssigns).where(inArray(permissionAssigns.roleId, roleIds));
    if (!assignRows.length) return [];

    const permissionIds = assignRows.map((item) => item.permissionId);
    const permissionRows = await db.select().from(permissions).where(inArray(permissions.id, permissionIds));
    const menuIds = permissionRows.map((item) => item.menuId).filter(Boolean) as string[];
    if (!menuIds.length) return [];

    const menuRows = await db.select().from(menus).where(inArray(menus.id, menuIds)).orderBy(asc(menus.seq));
    return buildTree(menuRows);
  });
}
