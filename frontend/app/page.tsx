import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowRight } from "lucide-react";

// Mock posts data for now - in production this would come from API
const mockPosts = [
  {
    id: 1,
    title: "Getting Started with FastAPI",
    content: "FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.",
    author: { name: "John Doe" },
    created_at: "2024-01-15T10:30:00Z"
  },
  {
    id: 2,
    title: "Building Modern UIs with Next.js",
    content: "Next.js gives you the best developer experience with all the features you need for production: hybrid static & server rendering, TypeScript support, smart bundling, route pre-fetching, and more.",
    author: { name: "Jane Smith" },
    created_at: "2024-01-14T15:45:00Z"
  },
  {
    id: 3,
    title: "Styling with Tailwind CSS",
    content: "A utility-first CSS framework packed with classes like flex, pt-4, text-center and rotate-90 that can be composed to build any design, directly in your markup.",
    author: { name: "Bob Johnson" },
    created_at: "2024-01-13T09:20:00Z"
  }
];

export default function HomePage() {
  return (
    <main className="container mx-auto px-4 py-8">
      <div className="flex flex-col gap-6">
        <div className="text-center">
          <h1 className="text-4xl font-bold tracking-tight mb-2">
            Welcome to <span className="text-primary">MyApp</span>
          </h1>
          <p className="text-muted-foreground">
            Discover the latest posts from our community
          </p>
        </div>

        <div className="flex justify-between items-center">
          <h2 className="text-2xl font-semibold">Latest Posts</h2>
          <Button asChild>
            <Link href="/dashboard">
              Dashboard
              <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
          </Button>
        </div>

        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {mockPosts.map((post) => (
            <Card key={post.id} className="cursor-pointer hover:shadow-lg transition-shadow">
              <Link href={`/posts/${post.id}`}>
                <CardHeader>
                  <CardTitle className="line-clamp-2">{post.title}</CardTitle>
                  <CardDescription>
                    by {post.author.name} • {new Date(post.created_at).toLocaleDateString()}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground line-clamp-3">
                    {post.content}
                  </p>
                </CardContent>
              </Link>
            </Card>
          ))}
        </div>

        <div className="text-center">
          <Button variant="outline" asChild>
            <Link href="/posts">
              View All Posts
              <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
          </Button>
        </div>
      </div>
    </main>
  );
}
