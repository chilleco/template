'use client';

import { usePosts } from '@/features/posts/api/usePosts';
import { PostCard } from '@/features/posts/components/post-card';

export function PostsGallery() {
  const { data, isLoading } = usePosts();

  if (isLoading) {
    return <p className="mt-8 text-foreground/60">Loading posts...</p>;
  }

  if (!data?.length) {
    return <p className="mt-8 text-foreground/60">No posts yet.</p>;
  }

  return (
    <div className="mt-8 grid gap-6 md:grid-cols-2">
      {data.map(post => (
        <PostCard key={post.id} post={post} />
      ))}
    </div>
  );
}
