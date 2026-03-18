import { notFound } from "next/navigation";
import { getVideo, getRecurrence, getWorkoutHistories } from "@/lib/api";
import VideoDetailClient from "./VideoDetailClient";

export default async function VideoDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;

  let video;
  try {
    video = await getVideo(id);
  } catch {
    notFound();
  }

  const [recurrence, workoutHistories] = await Promise.all([
    getRecurrence(id),
    getWorkoutHistories(),
  ]);

  const videoWorkouts = workoutHistories.filter(
    (wh) => wh.video_id === video.id
  );

  return (
    <VideoDetailClient
      video={video}
      recurrence={recurrence}
      workoutHistories={videoWorkouts}
    />
  );
}
