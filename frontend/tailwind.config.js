import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      backgroundColor: {
        primary: "#0f172a",
        secondary: "#1e293b",
        tertiary: "#334155",
      },
      colors: {
        primary: {
          50: "#f8fafc",
          100: "#f1f5f9",
          500: "#6366f1",
          600: "#4f46e5",
          700: "#4338ca",
        },
        purple: {
          500: "#a855f7",
          600: "#9333ea",
          700: "#7e22ce",
        },
        accent: "#10b981",
      },
      boxShadow: {
        glow: "0 0 20px rgba(99, 102, 241, 0.3)",
        "glow-purple": "0 0 20px rgba(168, 85, 247, 0.3)",
      },
      backgroundImage: {
        "gradient-primary": "linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)",
        "gradient-subtle": "linear-gradient(180deg, #0f172a 0%, #1e293b 100%)",
      },
    },
  },
  plugins: [],
};
export default config;
