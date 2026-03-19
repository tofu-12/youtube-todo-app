"use client";

import { useState } from "react";
import { loginUser, registerUser } from "@/lib/api";
import { useAuth } from "@/lib/auth";

type Mode = "login" | "register";

export default function AuthPage() {
  const { login } = useAuth();
  const [mode, setMode] = useState<Mode>("login");
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const res =
        mode === "login"
          ? await loginUser(email)
          : await registerUser(email);
      login(res.id, res.email);
    } catch (err) {
      if (err instanceof Error) {
        if (err.message.includes("404")) {
          setError("このメールアドレスは登録されていません");
        } else if (err.message.includes("409")) {
          setError("このメールアドレスは既に登録されています");
        } else {
          setError("エラーが発生しました。入力内容を確認してください。");
        }
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-[60vh] items-center justify-center">
      <div className="w-full max-w-sm rounded-lg border bg-white p-6 shadow-sm">
        <h1 className="mb-6 text-center text-2xl font-bold text-gray-900">
          YouTube Todo
        </h1>

        <div className="mb-6 flex rounded-lg border">
          <button
            type="button"
            className={`flex-1 py-2 text-sm font-medium ${
              mode === "login"
                ? "bg-blue-600 text-white"
                : "text-gray-600 hover:text-gray-900"
            } rounded-l-lg`}
            onClick={() => {
              setMode("login");
              setError("");
            }}
          >
            ログイン
          </button>
          <button
            type="button"
            className={`flex-1 py-2 text-sm font-medium ${
              mode === "register"
                ? "bg-blue-600 text-white"
                : "text-gray-600 hover:text-gray-900"
            } rounded-r-lg`}
            onClick={() => {
              setMode("register");
              setError("");
            }}
          >
            新規登録
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label
              htmlFor="email"
              className="block text-sm font-medium text-gray-700"
            >
              メールアドレス
            </label>
            <input
              id="email"
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
              placeholder="example@email.com"
            />
          </div>

          {error && (
            <p className="text-sm text-red-600">{error}</p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-md bg-blue-600 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
          >
            {loading
              ? "処理中..."
              : mode === "login"
                ? "ログイン"
                : "新規登録"}
          </button>
        </form>
      </div>
    </div>
  );
}
