import { makeClient } from "@/generated/api/client";
import type { paths } from "@/generated/api/schema";

/** Строго типизированный клиент */
export const api = makeClient<paths>({
  baseUrl: process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/v1",
});

export type Fetcher = <T>(
  url: string,
  init?: RequestInit,
) => Promise<T>;

export const swrFetcher: Fetcher = (url) =>
  fetch(url).then((r) => r.json());
