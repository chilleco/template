import { Metadata } from "next";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowLeft } from "lucide-react";

// Post type definition
interface Post {
  id: number;
  title: string;
  content: string;
  author_id: number;
  created_at: string;
}

interface PostPageProps { 
  params: { id: string } 
}

// Generate meta tags for SEO (title, description) dynamically
export async function generateMetadata({ params }: PostPageProps): Promise<Metadata> {
  try {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/posts/${params.id}`);
    if (!res.ok) {
      return { title: "Post Not Found" };
    }
    const post: Post = await res.json();
    return { title: post.title, description: post.content.substring(0, 150) };
  } catch {
    return { title: "Post Not Found" };
  }
}

export default async function PostPage({ params }: PostPageProps) {
  try {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/posts/${params.id}`, { 
      cache: 'no-store' 
    });
    
    if (!res.ok) {
      return (
        <main className="container mx-auto px-4 py-8 max-w-2xl">
          <div className="text-center">
            <h1 className="text-2xl font-bold mb-4">Post Not Found</h1>
            <p className="text-muted-foreground mb-4">The post you're looking for doesn't exist.</p>
            <Button asChild>
              <Link href="/posts">
                <ArrowLeft className="mr-2 h-4 w-4" />
                Back to Posts
              </Link>
            </Button>
          </div>
        </main>
      );
    }
    
    const post: Post = await res.json();
    
    return (
      <main className="container mx-auto px-4 py-8 max-w-2xl">
        <div className="flex flex-col gap-6">
          <Button variant="outline" size="sm" asChild className="self-start">
            <Link href="/posts">
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back to Posts
            </Link>
          </Button>
          
          <Card>
            <CardHeader>
              <CardTitle className="text-3xl">{post.title}</CardTitle>
              <CardDescription>
                Author ID: {post.author_id} • Published on {new Date(post.created_at).toLocaleDateString()}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="prose prose-gray max-w-none">
                <p className="whitespace-pre-line text-foreground leading-relaxed">
                  {post.content}
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    );
  } catch {
    return (
      <main className="container mx-auto px-4 py-8 max-w-2xl">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4">Error Loading Post</h1>
          <p className="text-muted-foreground mb-4">There was an error loading the post.</p>
          <Button asChild>
            <Link href="/posts">
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back to Posts
            </Link>
          </Button>
        </div>
      </main>
    );
  }
}
