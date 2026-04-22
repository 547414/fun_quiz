import { z } from "zod";

export const apiEnvelopeSchema = <T extends z.ZodTypeAny>(dataSchema: T) =>
  z.object({
    code: z.number(),
    message: z.string(),
    data: dataSchema,
  });

export const pageSchema = <T extends z.ZodTypeAny>(itemSchema: T) =>
  z.object({
    total: z.number().int().nonnegative(),
    list: z.array(itemSchema),
  });

export type ApiEnvelope<T> = {
  code: number;
  message: string;
  data: T;
};
