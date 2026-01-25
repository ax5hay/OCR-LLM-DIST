import "../globals.css";
import { Metadata } from "next";

export const metadata: Metadata = {
  title: "OCR-LLM Chat",
  description: "Beautiful AI-powered OCR and chat interface with LMStudio",
  icons: {
    icon: "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='75' font-size='75' fill='%236366f1'>◆</text></svg>",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <head>
        <style>{`
          :root {
            --background: 15 23 42;
            --foreground: 248 250 252;
            --primary: 99 102 241;
            --primary-foreground: 15 23 42;
            --secondary: 30 41 59;
            --secondary-foreground: 248 250 252;
            --destructive: 239 68 68;
            --destructive-foreground: 15 23 42;
            --muted: 100 116 139;
            --muted-foreground: 226 232 240;
            --accent: 16 185 129;
            --accent-foreground: 15 23 42;
            --border: 30 41 59;
            --input: 30 41 59;
            --ring: 99 102 241;
            --popover: 15 23 42;
            --popover-foreground: 248 250 252;
            --card: 15 23 42;
            --card-foreground: 248 250 252;
            --font-sans: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif;
          }

          * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
          }

          html, body {
            height: 100%;
            width: 100%;
            overflow: hidden;
          }

          body {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #f1f5f9;
            font-family: var(--font-sans);
          }

          ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
          }

          ::-webkit-scrollbar-track {
            background: rgba(30, 41, 59, 0.5);
          }

          ::-webkit-scrollbar-thumb {
            background: rgba(99, 102, 241, 0.6);
            border-radius: 4px;
          }

          ::-webkit-scrollbar-thumb:hover {
            background: rgba(99, 102, 241, 0.8);
          }
        `}</style>
      </head>
      <body>
        <div className="flex h-screen w-screen overflow-hidden bg-gradient-to-br from-slate-950 to-slate-900">
          {children}
        </div>
      </body>
    </html>
  );
}
