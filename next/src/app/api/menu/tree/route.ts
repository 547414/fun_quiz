import { asc } from "drizzle-orm";

import { db } from "@/db";
import { menus } from "@/db/schema/core";
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
    await requireAuth();
    const list = await db.select().from(menus).orderBy(asc(menus.seq), asc(menus.createdAt));
    const tree = buildTree(list);
    return {
      total: tree.length,
      list: tree,
    };
  });
}
