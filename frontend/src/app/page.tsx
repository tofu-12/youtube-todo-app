"use client";

import { useEffect, useState } from "react";
import { getTodayVideos } from "@/lib/api";
import TodoItem from "@/components/TodoItem";
import type { TodayVideoOut } from "@/lib/types";

export default function HomePage() {
  const [videos, setVideos] = useState<TodayVideoOut[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getTodayVideos()
      .then(setVideos)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <p className="text-gray-500">読み込み中...</p>;
  }

  return (
    <div>
      <h1 className="mb-4 text-xl font-bold text-gray-900 md:mb-6 md:text-2xl">今日のTODO</h1>
      {videos.length === 0 ? (
        <p className="text-gray-500">今日のTODOはありません</p>
      ) : (
        <div className="space-y-3">
          {videos.map((video) => (
            <TodoItem key={video.id} video={video} />
          ))}
        </div>
      )}
    </div>
  );
}
