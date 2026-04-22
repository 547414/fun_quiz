import { eq } from "drizzle-orm";

import { db } from "@/db";
import { inviteCodes } from "@/db/schema/core";
import { withApi } from "@/lib/http";

type Props = {
  params: Promise<{ inviteCodeId: string }>;
};

export async function GET(_: Request, props: Props) {
  return withApi(async () => {
    const { inviteCodeId } = await props.params;
    const [row] = await db.select().from(inviteCodes).where(eq(inviteCodes.id, inviteCodeId)).limit(1);
    return row ?? null;
  });
}
