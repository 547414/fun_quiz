import { desc } from "drizzle-orm";

import { db } from "@/db";
import { inviteCodes } from "@/db/schema/core";
import { requireAuth } from "@/lib/auth/guard";
import { withApi } from "@/lib/http";

export async function POST() {
  return withApi(async () => {
    await requireAuth(["SUPER_ADMIN", "ADMIN"]);
    const list = await db.select().from(inviteCodes).orderBy(desc(inviteCodes.createdAt));
    return {
      total: list.length,
      list,
    };
  });
}
