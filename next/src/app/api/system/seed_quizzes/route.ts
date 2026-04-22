import { requireAuth } from "@/lib/auth/guard";
import { env } from "@/lib/env";
import { AppError } from "@/lib/errors";
import { withApi } from "@/lib/http";
import { seedQuizzesFromPythonGenerated } from "@/server/bootstrap/quiz-seed";

export async function POST() {
  return withApi(async () => {
    const isProd = process.env.NODE_ENV === "production";
    if (isProd && env.BOOTSTRAP_ALLOW_IN_PROD !== "true") {
      throw new AppError("Quiz seed is disabled in production", 403);
    }

    await requireAuth(["SUPER_ADMIN", "ADMIN"]);
    return seedQuizzesFromPythonGenerated();
  });
}
