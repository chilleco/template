import './globals.css';

import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'AI Native Project Template',
  description: 'Full-stack baseline tuned for AI-assisted development workflows.'
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html suppressHydrationWarning lang="en">
      <body>{children}</body>
    </html>
  );
}
