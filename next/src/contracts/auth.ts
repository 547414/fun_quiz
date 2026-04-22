import { z } from "zod";

export const unionUserInfoSchema = z.object({
  unionUserId: z.string(),
  userId: z.string(),
  account: z.string(),
  name: z.string(),
  roleCodeList: z.array(z.string()),
  currentRoleCode: z.string().optional(),
  accessToken: z.string(),
  refreshToken: z.string(),
  scene: z.string(),
  space: z.string(),
});

export const loginRequestSchema = z.object({
  account: z.string().min(1),
  password: z.string().min(1),
  scene: z.string().default("WEB"),
  space: z.string().default("WEB"),
});

export const loginResponseSchema = z.object({
  unionUserInfo: unionUserInfoSchema,
  union_user_info: unionUserInfoSchema.optional(),
});

export const refreshRequestSchema = z.object({
  refreshToken: z.string().optional(),
});

export const refreshResponseSchema = z.object({
  accessToken: z.string(),
  refreshToken: z.string(),
  tokenType: z.string(),
  scene: z.string(),
  space: z.string(),
  unionUserInfo: unionUserInfoSchema.optional(),
  union_user_info: unionUserInfoSchema.optional(),
});

export type LoginRequest = z.infer<typeof loginRequestSchema>;
export type LoginResponse = z.infer<typeof loginResponseSchema>;
