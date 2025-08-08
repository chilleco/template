// frontend/app/posts/[id]/page.tsx
import { Metadata } from "next";
import { Post } from "../../../types/api";  // TypeScript type generated from OpenAPI

interface PostPageProps { params: { id: string } }

// Generate meta tags for SEO (title, description) dynamically
export async function generateMetadata({ params }: PostPageProps): Promise<Metadata> {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/posts/${params.id}`);
  if (!res.ok) {
    return { title: "Post Not Found" };
  }
  const post: Post = await res.json();
  return { title: post.title, description: post.content.substring(0, 150) };
}

export default async function PostPage({ params }: PostPageProps) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/posts/${params.id}`, { cache: 'no-store' });
  if (!res.ok) {
    // If the post is not found, you could throw notFound() for Next to render a 404 page
    return <h1>Post not found</h1>;
  }
  const post: Post = await res.json();
  return (
    <main className="max-w-2xl mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">{post.title}</h1>
      <p className="text-gray-700 whitespace-pre-line">{post.content}</p>
    </main>
  );
}
