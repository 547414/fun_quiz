import { NextResponse } from "next/server";

import { AppError, toErrorMessage } from "@/lib/errors";

type AsyncHandler<T> = () => Promise<T>;

export async function withApi<T>(handler: AsyncHandler<T>) {
  try {
    const data = await handler();
    return NextResponse.json({
      code: 200,
      message: "success",
      data,
    });
  } catch (error) {
    if (error instanceof AppError) {
      return NextResponse.json(
        {
          code: error.code,
          message: error.message,
          data: null,
        },
        { status: error.code >= 400 && error.code <= 599 ? error.code : 500 },
      );
    }
    return NextResponse.json(
      {
        code: 500,
        message: toErrorMessage(error),
        data: null,
      },
      { status: 500 },
    );
  }
}
