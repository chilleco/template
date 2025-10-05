"use client";

import Link from "next/link";

import { Button } from "@/components/ui/button";
import { usePostsList } from "@/features/posts/api";

export default function PostsView() {
  const { data, isLoading, isError } = usePostsList();

  if (isLoading) {
    return <p>Loading posts…</p>;
  }

  if (isError || !data?.length) {
    return (
      <div className="rounded-lg border p-6 text-center text-muted-foreground">
        <p>No posts yet.</p>
        <Button className="mt-4">Create first post</Button>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {data.map((post) => (
        <article key={post.id} className="rounded-lg border p-4 shadow-sm">
          <h2 className="text-xl font-semibold">{post.title}</h2>
          <p className="text-sm text-muted-foreground">{post.summary ?? "No summary"}</p>
          <div className="mt-3 flex justify-between text-sm text-muted-foreground">
            <span>{post.locale.toUpperCase()}</span>
            <span>{post.is_published ? "Published" : "Draft"}</span>
          </div>
          <Button asChild className="mt-4" variant="outline">
            <Link href={`/app/posts/${post.slug}`}>Open</Link>
          </Button>
        </article>
      ))}
    </div>
  );
}
