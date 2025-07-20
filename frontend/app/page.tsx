import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";

export default function LandingPage() {
  return (
    <main className="flex min-h-[calc(100vh-4rem)] flex-col items-center justify-center gap-6 px-6">
      <h1 className="text-center text-5xl font-extrabold tracking-tight">
        Welcome to <span className="text-primary">MyApp</span>
      </h1>

      <p className="max-w-xl text-center text-muted-foreground">
        The fastest way to bootstrap a modern web product —
        FastAPI × Next.js × shadcn/ui × OpenAPI-typed client.
      </p>

      <Button asChild size="lg">
        <Link href="/dashboard">
          Enter dashboard
          <ArrowRight className="ml-2 h-4 w-4" />
        </Link>
      </Button>
    </main>
  );
}
