import { entryRequestSchema } from "@/contracts/quiz-play";
import { AppError } from "@/lib/errors";
import { withApi } from "@/lib/http";
import { parseJsonBodyOrDefault } from "@/lib/request";
import { getEntryHistoryPage } from "@/server/services/quiz-service";

export async function POST(request: Request) {
  return withApi(async () => {
    const rawBody = await parseJsonBodyOrDefault(request, entryRequestSchema.partial(), {});
    const body = entryRequestSchema.parse(rawBody);
    if (!body.token) {
      throw new AppError("token is required", 400);
    }
    try {
      return await getEntryHistoryPage(body);
    } catch (error) {
      if ((error instanceof AppError && error.message === "Invalid token") || (error instanceof Error && error.message === "Invalid token")) {
        return {
          total: 0,
          list: [],
        };
      }
      throw error;
    }
  });
}
