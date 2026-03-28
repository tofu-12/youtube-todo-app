"use client";

import { useEffect, useState } from "react";
import { getOverdueVideos } from "@/lib/api";
import TodoItem from "@/components/TodoItem";
import type { TodayVideoOut } from "@/lib/types";

export default function OverduePage() {
  const [videos, setVideos] = useState<TodayVideoOut[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getOverdueVideos()
      .then(setVideos)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <p className="text-gray-500">読み込み中...</p>;
  }

  return (
    <div>
      <h1 className="mb-4 text-xl font-bold text-gray-900 md:mb-6 md:text-2xl">未実施</h1>
      {videos.length === 0 ? (
        <p className="text-gray-500">未実施の動画はありません</p>
      ) : (
        <div className="space-y-3">
          {videos.map((video) => (
            <TodoItem key={video.id} video={video} isOverdue />
          ))}
        </div>
      )}
    </div>
  );
}
