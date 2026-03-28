import type { Metadata } from "next";
import "./globals.css";
import { AuthProvider } from "@/lib/auth";
import NavBar from "@/components/NavBar";

export const metadata: Metadata = {
  title: "YouTube Todo App",
  description: "YouTube筋トレ動画管理TODOアプリ",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ja">
      <body className="min-h-screen bg-gray-50">
        <AuthProvider>
          <NavBar />
          <main className="mx-auto max-w-4xl px-4 py-4 md:py-8">{children}</main>
        </AuthProvider>
      </body>
    </html>
  );
}
