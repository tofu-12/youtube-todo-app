"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import type { VideoOut, RecurrenceOut, WorkoutHistoryOut } from "@/lib/types";
import { RecurrenceType } from "@/lib/types";
import { deleteVideo } from "@/lib/api";
import VideoForm from "@/components/VideoForm";

const RECURRENCE_LABELS: Record<RecurrenceType, string> = {
  [RecurrenceType.NONE]: "なし",
  [RecurrenceType.DAILY]: "毎日",
  [RecurrenceType.WEEKLY]: "毎週",
  [RecurrenceType.INTERVAL]: "間隔指定",
};

export default function VideoDetailClient({
  video,
  recurrence,
  workoutHistories,
}: {
  video: VideoOut;
  recurrence: RecurrenceOut | null;
  workoutHistories: WorkoutHistoryOut[];
}) {
  const router = useRouter();
  const [editing, setEditing] = useState(false);
  const [deleting, setDeleting] = useState(false);

  const handleDelete = async () => {
    if (!confirm("この動画を削除しますか？")) return;
    setDeleting(true);
    try {
      await deleteVideo(video.id);
      router.push("/videos");
      router.refresh();
    } catch (e) {
      alert(e instanceof Error ? e.message : "エラーが発生しました");
      setDeleting(false);
    }
  };

  if (editing) {
    return (
      <div>
        <div className="mb-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold text-gray-900">動画編集</h1>
          <button
            onClick={() => setEditing(false)}
            className="text-sm text-gray-500 hover:text-gray-700"
          >
            キャンセル
          </button>
        </div>
        <VideoForm
          mode="edit"
          initialData={video}
          initialRecurrence={recurrence}
        />
      </div>
    );
  }

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">{video.name}</h1>
        <div className="flex gap-2">
          <button
            onClick={() => setEditing(true)}
            className="rounded bg-blue-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-blue-700"
          >
            編集
          </button>
          <button
            onClick={handleDelete}
            disabled={deleting}
            className="rounded bg-red-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-red-700 disabled:opacity-50"
          >
            削除
          </button>
        </div>
      </div>

      <div className="space-y-6">
        <section className="rounded-lg border bg-white p-4">
          <h2 className="mb-3 font-semibold text-gray-900">動画情報</h2>
          <dl className="space-y-2 text-sm">
            <div>
              <dt className="text-gray-500">URL</dt>
              <dd>
                <a
                  href={video.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:underline"
                >
                  {video.url}
                </a>
              </dd>
            </div>
            {video.comment && (
              <div>
                <dt className="text-gray-500">コメント</dt>
                <dd className="text-gray-900">{video.comment}</dd>
              </div>
            )}
            {video.tags.length > 0 && (
              <div>
                <dt className="text-gray-500">タグ</dt>
                <dd className="flex flex-wrap gap-1 mt-1">
                  {video.tags.map((tag) => (
                    <span
                      key={tag.id}
                      className="inline-block rounded-full bg-blue-100 px-2 py-0.5 text-xs text-blue-800"
                    >
                      {tag.name}
                    </span>
                  ))}
                </dd>
              </div>
            )}
            <div>
              <dt className="text-gray-500">次回予定日</dt>
              <dd className="text-gray-900">
                {video.next_scheduled_date ?? "未設定"}
              </dd>
            </div>
            <div>
              <dt className="text-gray-500">最終実施日</dt>
              <dd className="text-gray-900">
                {video.last_performed_date ?? "未実施"}
              </dd>
            </div>
          </dl>
        </section>

        {recurrence && (
          <section className="rounded-lg border bg-white p-4">
            <h2 className="mb-3 font-semibold text-gray-900">繰り返しルール</h2>
            <p className="text-sm text-gray-900">
              {RECURRENCE_LABELS[recurrence.recurrence_type]}
              {recurrence.recurrence_type === RecurrenceType.INTERVAL &&
                recurrence.interval_days &&
                `（${recurrence.interval_days}日ごと）`}
              {recurrence.recurrence_type === RecurrenceType.WEEKLY &&
                recurrence.weekdays.length > 0 &&
                `（${recurrence.weekdays.join(", ")}）`}
            </p>
          </section>
        )}

        <section className="rounded-lg border bg-white p-4">
          <h2 className="mb-3 font-semibold text-gray-900">ワークアウト履歴</h2>
          {workoutHistories.length === 0 ? (
            <p className="text-sm text-gray-500">履歴がありません</p>
          ) : (
            <ul className="divide-y text-sm">
              {workoutHistories.map((wh) => (
                <li key={wh.id} className="py-2 text-gray-700">
                  {wh.performed_date}（有効期限: {wh.expires_date}）
                </li>
              ))}
            </ul>
          )}
        </section>
      </div>
    </div>
  );
}
