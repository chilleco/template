export function SiteFooter() {
  return (
    <footer className="border-t border-border bg-background/60 px-6 py-6 text-sm text-foreground/70">
      <p>Built for AI-first development workflows. © {new Date().getFullYear()}.</p>
    </footer>
  );
}
