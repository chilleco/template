import { type Config } from "tailwindcss";
import animate from "tailwindcss-animate";
import radix from "tailwindcss-radix";

export default {
  content: ["./src/**/*.{ts,tsx}", "../../backend/templates/**/*.html"],
  theme: {
    container: { center: true, padding: "1rem" },
    extend: {
      colors: {
        border: "hsl(var(--border) / <alpha-value>)",
        background: "hsl(var(--background) / <alpha-value>)",
        primary: "hsl(var(--primary) / <alpha-value>)",
      },
      borderRadius: { lg: "var(--radius)" },
    },
    fontFamily: { sans: ["var(--font-sans)", "sans-serif"] },
  },
  plugins: [animate, radix],
} satisfies Config;
