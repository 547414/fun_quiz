import { z, type ZodTypeAny } from "zod";

import { AppError } from "@/lib/errors";

export async function parseJsonBody<TSchema extends ZodTypeAny>(request: Request, schema: TSchema): Promise<z.infer<TSchema>> {
  const json = await request.json().catch(() => {
    throw new AppError("Invalid JSON body", 400);
  });
  const parsed = schema.safeParse(json);
  if (!parsed.success) {
    throw new AppError(parsed.error.issues[0]?.message ?? "Invalid request payload", 400, parsed.error.issues);
  }
  return parsed.data;
}

export async function parseJsonBodyOrDefault<TSchema extends ZodTypeAny>(
  request: Request,
  schema: TSchema,
  defaultValue: z.infer<TSchema>,
): Promise<z.infer<TSchema>> {
  const raw = await request.text().catch(() => "");
  if (!raw.trim()) {
    return defaultValue;
  }

  const json = (() => {
    try {
      return JSON.parse(raw) as unknown;
    } catch {
      throw new AppError("Invalid JSON body", 400);
    }
  })();
  const parsed = schema.safeParse(json);
  if (!parsed.success) {
    throw new AppError(parsed.error.issues[0]?.message ?? "Invalid request payload", 400, parsed.error.issues);
  }
  return parsed.data;
}
