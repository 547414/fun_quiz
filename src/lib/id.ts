import { v4 as uuidV4 } from "uuid";

export function createId() {
  return uuidV4().replaceAll("-", "");
}
