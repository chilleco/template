import { useQuery } from "@tanstack/react-query";

import { useApiClient } from "@/lib/api";

interface PostItem {
  id: string;
  title: string;
  slug: string;
  summary?: string | null;
  locale: string;
  is_published: boolean;
}

export function usePostsList() {
  const client = useApiClient();
  return useQuery({
    queryKey: ["posts"],
    queryFn: async () => {
      const response = await client.post<{ items: PostItem[]; meta: { next_cursor?: string | null } }>(
        "/api/v1/posts/list",
        { limit: 20 }
      );
      return response.items;
    }
  });
}
