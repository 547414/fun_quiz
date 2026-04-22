import { db } from "@/db";
import { roles } from "@/db/schema/core";
import { requireAuth } from "@/lib/auth/guard";
import { withApi } from "@/lib/http";

export async function GET() {
  return withApi(async () => {
    await requireAuth(["SUPER_ADMIN", "ADMIN"]);
    const list = await db.select().from(roles);
    return {
      total: list.length,
      enabledTotal: list.filter((item) => item.enabled).length,
      disabledTotal: list.filter((item) => !item.enabled).length,
    };
  });
}
