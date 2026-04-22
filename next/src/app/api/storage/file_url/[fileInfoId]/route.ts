import { eq } from "drizzle-orm";

import { db } from "@/db";
import { fileInfos } from "@/db/schema/core";
import { requireAuth } from "@/lib/auth/guard";
import { withApi } from "@/lib/http";

type Props = {
  params: Promise<{ fileInfoId: string }>;
};

export async function GET(_: Request, props: Props) {
  return withApi(async () => {
    await requireAuth();
    const { fileInfoId } = await props.params;
    const [row] = await db.select().from(fileInfos).where(eq(fileInfos.id, fileInfoId)).limit(1);
    if (!row) return null;
    return {
      ...row,
      fileUrl: `/${row.storageKey}`,
    };
  });
}
