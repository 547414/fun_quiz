export type ApiResponseShape<T = unknown> = {
  code: number;
  message: string;
  data: T;
};

export function ok<T>(data: T, message = "success"): ApiResponseShape<T> {
  return {
    code: 200,
    message,
    data,
  };
}

export function fail(message: string, code = 500): ApiResponseShape<null> {
  return {
    code,
    message,
    data: null,
  };
}
