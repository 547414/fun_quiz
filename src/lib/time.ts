export function parseExpiresInToSeconds(input: string): number {
  const value = input.trim().toLowerCase();
  const matched = value.match(/^(\d+)(s|m|h|d)$/);
  if (!matched) return 7200;
  const amount = Number(matched[1]);
  const unit = matched[2];
  if (unit === "s") return amount;
  if (unit === "m") return amount * 60;
  if (unit === "h") return amount * 3600;
  return amount * 86400;
}
