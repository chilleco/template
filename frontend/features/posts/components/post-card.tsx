import Link from 'next/link';

import { Card, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import type { Post } from '@/lib/schemas/post';
import { cn } from '@/lib/utils';

interface Props {
  post: Post;
  className?: string;
}

export function PostCard({ post, className }: Props) {
  return (
    <Card className={cn('h-full rounded-xl border border-border/80 bg-background p-6', className)}>
      <CardHeader className="space-y-2">
        <CardTitle className="text-xl">
          <Link href={`/${post.locale}/posts/${post.slug}`} className="hover:underline">
            {post.title}
          </Link>
        </CardTitle>
        {post.summary ? <CardDescription>{post.summary}</CardDescription> : null}
      </CardHeader>
      <p className="text-xs uppercase text-foreground/60">{post.status}</p>
    </Card>
  );
}
