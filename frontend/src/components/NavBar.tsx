"use client";

import Link from "next/link";
import { useAuth } from "@/lib/auth";

const navItems = [
  { href: "/", label: "今日のTODO" },
  { href: "/overdue", label: "未実施" },
  { href: "/calendar", label: "カレンダー" },
  { href: "/videos", label: "動画一覧" },
  { href: "/videos/new", label: "動画登録" },
  { href: "/settings", label: "設定" },
];

export default function NavBar() {
  const { userId, email, logout } = useAuth();

  return (
    <nav className="bg-white shadow">
      <div className="mx-auto max-w-4xl px-4">
        <div className="flex h-14 items-center gap-6">
          <span className="font-bold text-lg text-gray-900">YouTube Todo</span>
          {userId && (
            <>
              {navItems.map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  className="text-sm text-gray-600 hover:text-gray-900"
                >
                  {item.label}
                </Link>
              ))}
              <div className="ml-auto flex items-center gap-3">
                <span className="text-xs text-gray-500">{email}</span>
                <button
                  type="button"
                  onClick={logout}
                  className="rounded bg-gray-200 px-3 py-1 text-xs text-gray-700 hover:bg-gray-300"
                >
                  ログアウト
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}
