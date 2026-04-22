import { desc } from "drizzle-orm";

import { db } from "@/db";
import { backendApis } from "@/db/schema/core";
import { requireAuth } from "@/lib/auth/guard";
import { withApi } from "@/lib/http";

export async function POST() {
  return withApi(async () => {
    await requireAuth(["SUPER_ADMIN"]);
    const list = await db.select().from(backendApis).orderBy(desc(backendApis.createdAt));
    return {
      total: list.length,
      list,
    };
  });
}
