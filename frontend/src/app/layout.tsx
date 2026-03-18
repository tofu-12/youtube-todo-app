import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "YouTube Todo App",
  description: "YouTube筋トレ動画管理TODOアプリ",
};

const navItems = [
  { href: "/", label: "今日のTODO" },
  { href: "/overdue", label: "未実施" },
  { href: "/videos", label: "動画一覧" },
  { href: "/videos/new", label: "動画登録" },
];

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ja">
      <body className="min-h-screen bg-gray-50">
        <nav className="bg-white shadow">
          <div className="mx-auto max-w-4xl px-4">
            <div className="flex h-14 items-center gap-6">
              <span className="font-bold text-lg text-gray-900">
                YouTube Todo
              </span>
              {navItems.map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  className="text-sm text-gray-600 hover:text-gray-900"
                >
                  {item.label}
                </Link>
              ))}
            </div>
          </div>
        </nav>
        <main className="mx-auto max-w-4xl px-4 py-8">{children}</main>
      </body>
    </html>
  );
}
