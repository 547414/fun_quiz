import { createId } from "@/lib/id";
import { withApi } from "@/lib/http";

export async function POST() {
  return withApi(async () => {
    return {
      verifyId: createId(),
      imgBase64: "",
      textList: ["山", "海", "风"],
      tip: "请按顺序点击文字（开发占位）",
    };
  });
}
