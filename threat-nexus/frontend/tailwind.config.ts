import type { Config } from "tailwindcss";

export default {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        background: "#080b0f",
        panel: "#111820",
        border: "#25313d",
        accent: "#38bdf8",
        danger: "#ef4444"
      }
    },
  },
  plugins: [],
} satisfies Config;
