import { Suspense } from 'react';

import { PostsGallery } from '@/components/posts/posts-gallery';

export default function PostsPage() {
  return (
    <section className="mx-auto w-full max-w-5xl px-6 py-12">
      <h1 className="text-3xl font-semibold">Latest posts</h1>
      <p className="mt-2 text-foreground/70">SEO-ready, localized content managed with strict access controls.</p>
      <Suspense fallback={<p className="mt-8 text-foreground/60">Loading posts...</p>}>
        <PostsGallery />
      </Suspense>
    </section>
  );
}
