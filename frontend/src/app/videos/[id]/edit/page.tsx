"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { getVideo, getRecurrence } from "@/lib/api";
import VideoForm from "@/components/VideoForm";
import type { VideoOut, RecurrenceOut } from "@/lib/types";

export default function VideoEditPage() {
  const params = useParams<{ id: string }>();
  const [video, setVideo] = useState<VideoOut | null>(null);
  const [recurrence, setRecurrence] = useState<RecurrenceOut | null>(null);
  const [loading, setLoading] = useState(true);
  const [notFound, setNotFound] = useState(false);

  useEffect(() => {
    async function load() {
      try {
        const [v, r] = await Promise.all([
          getVideo(params.id),
          getRecurrence(params.id),
        ]);
        setVideo(v);
        setRecurrence(r);
      } catch {
        setNotFound(true);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [params.id]);

  if (loading) return <p className="text-gray-500">読み込み中...</p>;
  if (notFound || !video)
    return <p className="text-gray-500">動画が見つかりません</p>;

  return (
    <div>
      <div className="mb-4 flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">動画編集</h1>
        <Link
          href={`/videos/${params.id}`}
          className="text-sm text-gray-500 hover:text-gray-700"
        >
          キャンセル
        </Link>
      </div>
      <VideoForm
        mode="edit"
        initialData={video}
        initialRecurrence={recurrence}
      />
    </div>
  );
}
