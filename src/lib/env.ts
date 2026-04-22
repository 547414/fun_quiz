import { z } from "zod";

const envSchema = z.object({
  DATABASE_URL: z.string().min(1).default("postgresql://invalid:invalid@localhost:5432/invalid"),
  APP_JWT_SECRET: z.string().min(16).default("replace-with-at-least-16-characters"),
  APP_JWT_EXPIRES_IN: z.string().default("2h"),
  NEXT_PUBLIC_APP_NAME: z.string().default("Fun Quiz"),
  BOOTSTRAP_SETUP_SECRET: z.string().optional(),
  BOOTSTRAP_ALLOW_IN_PROD: z.string().default("false"),
});

export const env = envSchema.parse({
  DATABASE_URL: process.env.DATABASE_URL,
  APP_JWT_SECRET: process.env.APP_JWT_SECRET,
  APP_JWT_EXPIRES_IN: process.env.APP_JWT_EXPIRES_IN,
  NEXT_PUBLIC_APP_NAME: process.env.NEXT_PUBLIC_APP_NAME,
  BOOTSTRAP_SETUP_SECRET: process.env.BOOTSTRAP_SETUP_SECRET,
  BOOTSTRAP_ALLOW_IN_PROD: process.env.BOOTSTRAP_ALLOW_IN_PROD,
});
