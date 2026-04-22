import { describe, expect, it } from "vitest";

import { parseExpiresInToSeconds } from "@/lib/time";

describe("parseExpiresInToSeconds", () => {
  it("支持小时和分钟", () => {
    expect(parseExpiresInToSeconds("2h")).toBe(7200);
    expect(parseExpiresInToSeconds("15m")).toBe(900);
  });

  it("无效输入使用默认值", () => {
    expect(parseExpiresInToSeconds("invalid")).toBe(7200);
  });
});
