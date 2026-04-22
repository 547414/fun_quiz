import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function toBoolean(input: unknown): boolean {
  if (typeof input === "boolean") return input;
  if (typeof input === "string") {
    return ["1", "true", "yes", "on"].includes(input.toLowerCase());
  }
  if (typeof input === "number") return input > 0;
  return false;
}
