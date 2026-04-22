import { eq } from "drizzle-orm";

import { db } from "@/db";
import { organizations } from "@/db/schema/core";
import { requireAuth } from "@/lib/auth/guard";
import { withApi } from "@/lib/http";

type Props = {
  params: Promise<{ organizationId: string }>;
};

export async function GET(_: Request, props: Props) {
  return withApi(async () => {
    await requireAuth();
    const { organizationId } = await props.params;
    const [row] = await db.select().from(organizations).where(eq(organizations.id, organizationId)).limit(1);
    return row ?? null;
  });
}
