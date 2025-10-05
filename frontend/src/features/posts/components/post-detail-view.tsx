"use client";

import { useQuery } from "@tanstack/react-query";

import { Button } from "@/components/ui/button";
import { useApiClient } from "@/lib/api";

interface Props {
  slug: string;
}

export default function PostDetailView({ slug }: Props) {
  const client = useApiClient();
  const { data, isLoading, isError } = useQuery({
    queryKey: ["post", slug],
    queryFn: async () =>
      client.post<{ id: string; title: string; content: string; is_published: boolean }>(
        "/api/v1/posts/detail",
        { slug }
      )
  });

  if (isLoading) {
    return <p>Loading post…</p>;
  }

  if (isError || !data) {
    return <p>Unable to load post.</p>;
  }

  return (
    <article className="prose dark:prose-invert">
      <header className="mb-4 border-b pb-4">
        <h1>{data.title}</h1>
        <p className="text-sm text-muted-foreground">
          {data.is_published ? "Published" : "Draft"}
        </p>
      </header>
      <div dangerouslySetInnerHTML={{ __html: data.content }} />
      <Button className="mt-6" variant="outline">
        Update Post
      </Button>
    </article>
  );
}
