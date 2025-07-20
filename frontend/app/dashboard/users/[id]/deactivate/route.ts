import { NextRequest, NextResponse } from "next/server";
import { api } from "@/lib/api";

/**
 * POST /dashboard/users/[id]/deactivate (edge runtime, JSON)
 * Проксирует на бекенд, возвращает 204|404.
 */
export const runtime = "edge";

export async function POST(
  _req: NextRequest,
  { params }: { params: { id: string } },
) {
  const res = await api.POST("/users/{user_id}/deactivate", {
    params: { path: { user_id: params.id } },
  });

  return res.error
    ? NextResponse.json(res.error, { status: res.response?.status ?? 500 })
    : new NextResponse(null, { status: 204 });
}
