"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import type { TodayVideoOut } from "@/lib/types";
import { TodoStatus } from "@/lib/types";
import { createTodoHistory, createWorkoutHistory } from "@/lib/api";

export default function TodoItem({
  video,
  isOverdue = false,
}: {
  video: TodayVideoOut;
  isOverdue?: boolean;
}) {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [showSkipForm, setShowSkipForm] = useState(false);
  const [skipDate, setSkipDate] = useState("");

  const handleComplete = async () => {
    setLoading(true);
    try {
      await createTodoHistory({
        video_id: video.id,
        scheduled_date: video.next_scheduled_date!,
        status: isOverdue ? TodoStatus.SKIPPED : TodoStatus.COMPLETED,
      });
      if (!isOverdue) {
        await createWorkoutHistory({
          video_id: video.id,
        });
      }
      router.refresh();
    } catch (e) {
      alert(e instanceof Error ? e.message : "エラーが発生しました");
    } finally {
      setLoading(false);
    }
  };

  const handleSkipConfirm = async () => {
    setLoading(true);
    try {
      await createTodoHistory({
        video_id: video.id,
        scheduled_date: video.next_scheduled_date!,
        status: TodoStatus.SKIPPED,
        next_scheduled_date: skipDate,
      });
      setShowSkipForm(false);
      setSkipDate("");
      router.refresh();
    } catch (e) {
      alert(e instanceof Error ? e.message : "エラーが発生しました");
    } finally {
      setLoading(false);
    }
  };

  const handleSkipCancel = () => {
    setShowSkipForm(false);
    setSkipDate("");
  };

  return (
    <div className="rounded-lg border bg-white p-4 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0 flex-1">
          <h3 className="font-semibold text-gray-900">{video.name}</h3>
          {video.tags.length > 0 && (
            <div className="mt-1 flex flex-wrap gap-1">
              {video.tags.map((tag) => (
                <span
                  key={tag.id}
                  className="inline-block rounded-full bg-blue-100 px-2 py-0.5 text-xs text-blue-800"
                >
                  {tag.name}
                </span>
              ))}
            </div>
          )}
          {video.next_scheduled_date && (
            <p className="mt-1 text-sm text-gray-500">
              予定日: {video.next_scheduled_date}
            </p>
          )}
          {video.comment && (
            <p className="mt-1 text-sm text-gray-500">{video.comment}</p>
          )}
        </div>
        <div className="flex shrink-0 gap-2">
          <a
            href={video.url}
            target="_blank"
            rel="noopener noreferrer"
            className="rounded bg-red-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-red-700"
          >
            YouTube
          </a>
          <button
            onClick={handleComplete}
            disabled={loading}
            className="rounded bg-green-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-green-700 disabled:opacity-50"
          >
            完了
          </button>
          <button
            onClick={() => setShowSkipForm(true)}
            disabled={loading || showSkipForm}
            className="rounded bg-gray-400 px-3 py-1.5 text-sm font-medium text-white hover:bg-gray-500 disabled:opacity-50"
          >
            スキップ
          </button>
        </div>
      </div>
      {showSkipForm && (
        <div className="mt-3 flex items-center gap-2 border-t pt-3">
          <label className="text-sm text-gray-700">次回予定日:</label>
          <input
            type="date"
            value={skipDate}
            onChange={(e) => setSkipDate(e.target.value)}
            className="rounded border px-2 py-1 text-sm"
          />
          <button
            onClick={handleSkipConfirm}
            disabled={loading || !skipDate}
            className="rounded bg-blue-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
          >
            確定
          </button>
          <button
            onClick={handleSkipCancel}
            disabled={loading}
            className="rounded bg-gray-300 px-3 py-1.5 text-sm font-medium text-gray-700 hover:bg-gray-400 disabled:opacity-50"
          >
            キャンセル
          </button>
        </div>
      )}
    </div>
  );
}
