"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { getVideo, getRecurrence, getWorkoutHistories } from "@/lib/api";
import VideoDetailClient from "./VideoDetailClient";
import type { VideoOut, RecurrenceOut, WorkoutHistoryOut } from "@/lib/types";

export default function VideoDetailPage() {
  const params = useParams<{ id: string }>();
  const [video, setVideo] = useState<VideoOut | null>(null);
  const [recurrence, setRecurrence] = useState<RecurrenceOut | null>(null);
  const [workoutHistories, setWorkoutHistories] = useState<
    WorkoutHistoryOut[]
  >([]);
  const [loading, setLoading] = useState(true);
  const [notFound, setNotFound] = useState(false);

  useEffect(() => {
    const id = params.id;

    async function load() {
      try {
        const v = await getVideo(id);
        const [r, wh] = await Promise.all([
          getRecurrence(id),
          getWorkoutHistories(),
        ]);
        setVideo(v);
        setRecurrence(r);
        setWorkoutHistories(wh.filter((w) => w.video_id === v.id));
      } catch {
        setNotFound(true);
      } finally {
        setLoading(false);
      }
    }

    load();
  }, [params.id]);

  if (loading) {
    return <p className="text-gray-500">読み込み中...</p>;
  }

  if (notFound || !video) {
    return <p className="text-gray-500">動画が見つかりません</p>;
  }

  return (
    <VideoDetailClient
      video={video}
      recurrence={recurrence}
      workoutHistories={workoutHistories}
    />
  );
}
