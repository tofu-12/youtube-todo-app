"use client";

import { useEffect, useState } from "react";
import { getTodayVideos, getOverdueVideos } from "@/lib/api";
import TodoItem from "@/components/TodoItem";
import type { TodayVideoOut } from "@/lib/types";

type Tab = "today" | "overdue";

export default function HomePage() {
  const [tab, setTab] = useState<Tab>("today");
  const [todayVideos, setTodayVideos] = useState<TodayVideoOut[]>([]);
  const [overdueVideos, setOverdueVideos] = useState<TodayVideoOut[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getTodayVideos(), getOverdueVideos()])
      .then(([today, overdue]) => {
        setTodayVideos(today);
        setOverdueVideos(overdue);
      })
      .finally(() => setLoading(false));
  }, []);

  const activeVideos = tab === "today" ? todayVideos : overdueVideos;

  if (loading) {
    return <p className="text-gray-500">読み込み中...</p>;
  }

  return (
    <div>
      {/* Tab buttons */}
      <div className="mb-4 flex gap-2 md:mb-6">
        <button
          type="button"
          onClick={() => setTab("today")}
          className={`px-3 py-2 text-sm rounded md:py-1 ${
            tab === "today"
              ? "bg-gray-800 text-white"
              : "bg-gray-200 text-gray-700 hover:bg-gray-300"
          }`}
        >
          今日のTODO
        </button>
        <button
          type="button"
          onClick={() => setTab("overdue")}
          className={`px-3 py-2 text-sm rounded md:py-1 ${
            tab === "overdue"
              ? "bg-gray-800 text-white"
              : "bg-gray-200 text-gray-700 hover:bg-gray-300"
          }`}
        >
          未実施
        </button>
      </div>

      {/* Content */}
      {activeVideos.length === 0 ? (
        <p className="text-gray-500">
          {tab === "today"
            ? "今日のTODOはありません"
            : "未実施の動画はありません"}
        </p>
      ) : (
        <div className="space-y-3">
          {activeVideos.map((video) => (
            <TodoItem
              key={video.id}
              video={video}
              {...(tab === "overdue" ? { isOverdue: true } : {})}
            />
          ))}
        </div>
      )}
    </div>
  );
}
