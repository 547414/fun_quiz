import { db } from "@/db";
import { fileInfos } from "@/db/schema/core";
import { requireAuth } from "@/lib/auth/guard";
import { createId } from "@/lib/id";
import { withApi } from "@/lib/http";

export async function POST(request: Request) {
  return withApi(async () => {
    await requireAuth();
    const formData = await request.formData();
    const file = formData.get("file");
    if (!(file instanceof File)) {
      throw new Error("file is required");
    }
    const id = createId();
    const storageKey = `uploads/${id}/${file.name}`;
    await db.insert(fileInfos).values({
      id,
      storageKey,
      fileName: file.name,
      mimeType: file.type || null,
      size: file.size,
    });
    return {
      fileInfoId: id,
      storageKey,
      fileName: file.name,
    };
  });
}
