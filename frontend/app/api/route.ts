/**
 * GET /api — edge-runtime ping, возвращает “ok”.
 * Пример того, как в App Router делают внутренних API-ручки.
 */
export const runtime = "edge";

export async function GET() {
  return Response.json({ status: "ok", ts: Date.now() });
}
