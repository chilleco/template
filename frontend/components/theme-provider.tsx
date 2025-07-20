"use client";

import { ThemeProvider as NextThemes } from "next-themes";
import { ReactNode } from "react";

export function ThemeProvider({
  children,
  ...props
}: {
  children: ReactNode;
  attribute?: "class" | "data-theme";
  defaultTheme?: "system" | "dark" | "light";
  enableSystem?: boolean;
}) {
  return (
    <NextThemes attribute="class" defaultTheme="system" enableSystem {...props}>
      {children}
    </NextThemes>
  );
}
