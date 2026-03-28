"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
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
  const pathname = usePathname();
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <nav className="bg-white shadow">
      <div className="mx-auto max-w-4xl px-4">
        <div className="flex h-14 items-center justify-between md:gap-6">
          <span className="font-bold text-lg text-gray-900">YouTube Todo</span>
          {userId && (
            <>
              {/* Desktop nav links */}
              <div className="hidden md:flex md:items-center md:gap-6">
                {navItems.map((item) => (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={`text-sm ${
                      pathname === item.href
                        ? "font-medium text-blue-700"
                        : "text-gray-600 hover:text-gray-900"
                    }`}
                  >
                    {item.label}
                  </Link>
                ))}
              </div>

              {/* Desktop email + logout */}
              <div className="ml-auto hidden md:flex md:items-center md:gap-3">
                <span className="text-xs text-gray-500">{email}</span>
                <button
                  type="button"
                  onClick={logout}
                  className="rounded bg-gray-200 px-3 py-1 text-xs text-gray-700 hover:bg-gray-300"
                >
                  ログアウト
                </button>
              </div>

              {/* Mobile hamburger button */}
              <button
                type="button"
                className="flex min-h-[44px] min-w-[44px] items-center justify-center text-xl text-gray-600 hover:text-gray-900 md:hidden"
                onClick={() => setMenuOpen(!menuOpen)}
                aria-label="メニュー"
              >
                {menuOpen ? "✕" : "☰"}
              </button>
            </>
          )}
        </div>
      </div>

      {/* Mobile drawer */}
      {userId && menuOpen && (
        <div className="border-t border-gray-200 md:hidden">
          <div className="space-y-1 px-2 pb-2 pt-2">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => setMenuOpen(false)}
                className={`block rounded-md px-3 py-2 text-base ${
                  pathname === item.href
                    ? "bg-blue-50 font-medium text-blue-700"
                    : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
                }`}
              >
                {item.label}
              </Link>
            ))}
          </div>
          <div className="border-t border-gray-200 px-4 pb-3 pt-2">
            <p className="truncate text-xs text-gray-500">{email}</p>
            <button
              type="button"
              onClick={() => {
                setMenuOpen(false);
                logout();
              }}
              className="mt-2 w-full rounded bg-gray-200 px-3 py-2 text-sm text-gray-700 hover:bg-gray-300"
            >
              ログアウト
            </button>
          </div>
        </div>
      )}
    </nav>
  );
}
