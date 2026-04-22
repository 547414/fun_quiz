import { eq } from "drizzle-orm";

import { db } from "@/db";
import { menus } from "@/db/schema/core";
import { requireAuth } from "@/lib/auth/guard";
import { withApi } from "@/lib/http";

type Props = {
  params: Promise<{ menuId: string }>;
};

export async function GET(_: Request, props: Props) {
  return withApi(async () => {
    await requireAuth(["SUPER_ADMIN", "ADMIN"]);
    const { menuId } = await props.params;
    const [row] = await db.select().from(menus).where(eq(menus.id, menuId)).limit(1);
    return row ?? null;
  });
}
