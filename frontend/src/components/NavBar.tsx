"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/lib/auth";

const navItems = [
  { href: "/videos", label: "動画一覧" },
  { href: "/calendar", label: "カレンダー" },
];

const mobileNavItems = [
  { href: "/", label: "ホーム" },
  { href: "/videos", label: "動画一覧" },
  { href: "/calendar", label: "カレンダー" },
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
          <Link href="/" className="font-bold text-lg text-gray-900 hover:text-gray-700">
            YouTube Todo
          </Link>
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

              {/* Desktop email + logout + settings gear */}
              <div className="ml-auto hidden md:flex md:items-center md:gap-3">
                <span className="text-xs text-gray-500">{email}</span>
                <button
                  type="button"
                  onClick={logout}
                  className="rounded bg-gray-200 px-3 py-1 text-xs text-gray-700 hover:bg-gray-300"
                >
                  ログアウト
                </button>
                <Link
                  href="/settings"
                  className={`flex items-center ${
                    pathname === "/settings"
                      ? "text-blue-700"
                      : "text-gray-500 hover:text-gray-700"
                  }`}
                  aria-label="設定"
                >
                  <svg
                    className="h-5 w-5"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth={1.5}
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.325.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 0 1 1.37.49l1.296 2.247a1.125 1.125 0 0 1-.26 1.431l-1.003.827c-.293.241-.438.613-.43.992a7.723 7.723 0 0 1 0 .255c-.008.378.137.75.43.991l1.004.827c.424.35.534.955.26 1.43l-1.298 2.247a1.125 1.125 0 0 1-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.47 6.47 0 0 1-.22.128c-.331.183-.581.495-.644.869l-.213 1.281c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.019-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 0 1-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 0 1-1.369-.49l-1.297-2.247a1.125 1.125 0 0 1 .26-1.431l1.004-.827c.292-.24.437-.613.43-.991a6.932 6.932 0 0 1 0-.255c.007-.38-.138-.751-.43-.992l-1.004-.827a1.125 1.125 0 0 1-.26-1.43l1.297-2.247a1.125 1.125 0 0 1 1.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.086.22-.128.332-.183.582-.495.644-.869l.214-1.28Z"
                    />
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
                    />
                  </svg>
                </Link>
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
            {mobileNavItems.map((item) => (
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
