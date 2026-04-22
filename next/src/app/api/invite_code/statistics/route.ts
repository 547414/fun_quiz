import { db } from "@/db";
import { inviteCodes } from "@/db/schema/core";
import { withApi } from "@/lib/http";

export async function GET() {
  return withApi(async () => {
    const list = await db.select().from(inviteCodes);
    return {
      total: list.length,
      enabledTotal: list.filter((item) => item.enabled).length,
      usedTotal: list.reduce((acc, item) => acc + item.usedTimes, 0),
    };
  });
}
