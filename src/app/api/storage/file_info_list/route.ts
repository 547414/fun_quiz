import { inArray } from "drizzle-orm";
import { z } from "zod";

import { db } from "@/db";
import { fileInfos } from "@/db/schema/core";
import { requireAuth } from "@/lib/auth/guard";
import { withApi } from "@/lib/http";
import { parseJsonBody } from "@/lib/request";

const schema = z.object({
  fileInfoIdList: z.array(z.string()).default([]),
});

export async function POST(request: Request) {
  return withApi(async () => {
    await requireAuth();
    const { fileInfoIdList } = await parseJsonBody(request, schema);
    if (!fileInfoIdList.length) return [];
    return db.select().from(fileInfos).where(inArray(fileInfos.id, fileInfoIdList));
  });
}
