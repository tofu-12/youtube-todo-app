"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import type { VideoOut, RecurrenceOut } from "@/lib/types";
import { RecurrenceType, DayOfWeek } from "@/lib/types";
import { createVideo, updateVideo, upsertRecurrence } from "@/lib/api";

interface VideoFormProps {
  mode: "create" | "edit";
  initialData?: VideoOut;
  initialRecurrence?: RecurrenceOut | null;
}

const ALL_WEEKDAYS = [
  { value: DayOfWeek.MON, label: "月" },
  { value: DayOfWeek.TUE, label: "火" },
  { value: DayOfWeek.WED, label: "水" },
  { value: DayOfWeek.THU, label: "木" },
  { value: DayOfWeek.FRI, label: "金" },
  { value: DayOfWeek.SAT, label: "土" },
  { value: DayOfWeek.SUN, label: "日" },
];

export default function VideoForm({
  mode,
  initialData,
  initialRecurrence,
}: VideoFormProps) {
  const router = useRouter();
  const [loading, setLoading] = useState(false);

  const [name, setName] = useState(initialData?.name ?? "");
  const [url, setUrl] = useState(initialData?.url ?? "");
  const [comment, setComment] = useState(initialData?.comment ?? "");
  const [tagInput, setTagInput] = useState(
    initialData?.tags.map((t) => t.name).join(", ") ?? ""
  );
  const [nextScheduledDate, setNextScheduledDate] = useState(
    initialData?.next_scheduled_date ?? ""
  );

  const [recurrenceType, setRecurrenceType] = useState<RecurrenceType>(
    initialRecurrence?.recurrence_type ?? RecurrenceType.NONE
  );
  const [intervalDays, setIntervalDays] = useState<number>(
    initialRecurrence?.interval_days ?? 1
  );
  const [weekdays, setWeekdays] = useState<DayOfWeek[]>(
    initialRecurrence?.weekdays ?? []
  );

  const toggleWeekday = (day: DayOfWeek) => {
    setWeekdays((prev) =>
      prev.includes(day) ? prev.filter((d) => d !== day) : [...prev, day]
    );
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const tagNames = tagInput
        .split(",")
        .map((s) => s.trim())
        .filter(Boolean);

      let videoId: string;

      if (mode === "create") {
        const video = await createVideo({
          name,
          url,
          comment: comment || null,
          next_scheduled_date: nextScheduledDate || null,
          tag_names: tagNames,
        });
        videoId = video.id;
      } else {
        const video = await updateVideo(initialData!.id, {
          name,
          url,
          comment: comment || null,
          next_scheduled_date: nextScheduledDate || null,
          tag_names: tagNames,
        });
        videoId = video.id;
      }

      if (recurrenceType !== RecurrenceType.NONE) {
        await upsertRecurrence(videoId, {
          recurrence_type: recurrenceType,
          interval_days:
            recurrenceType === RecurrenceType.INTERVAL ? intervalDays : null,
          weekdays:
            recurrenceType === RecurrenceType.WEEKLY ? weekdays : [],
        });
      }

      if (mode === "create") {
        router.push("/videos");
      } else {
        router.push(`/videos/${videoId}`);
      }
      router.refresh();
    } catch (e) {
      alert(e instanceof Error ? e.message : "エラーが発生しました");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700">
          動画名
        </label>
        <input
          type="text"
          required
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">URL</label>
        <input
          type="url"
          required
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">
          コメント
        </label>
        <textarea
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          rows={3}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">
          タグ（カンマ区切り）
        </label>
        <input
          type="text"
          value={tagInput}
          onChange={(e) => setTagInput(e.target.value)}
          placeholder="例: 胸, 腕, 背中"
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">
          次回予定日
        </label>
        <input
          type="date"
          value={nextScheduledDate}
          onChange={(e) => setNextScheduledDate(e.target.value)}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        />
      </div>

      <fieldset className="rounded-md border p-4">
        <legend className="text-sm font-medium text-gray-700">
          繰り返し設定
        </legend>

        <div className="mt-2">
          <select
            value={recurrenceType}
            onChange={(e) =>
              setRecurrenceType(e.target.value as RecurrenceType)
            }
            className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          >
            <option value={RecurrenceType.NONE}>なし</option>
            <option value={RecurrenceType.DAILY}>毎日</option>
            <option value={RecurrenceType.WEEKLY}>毎週</option>
            <option value={RecurrenceType.INTERVAL}>間隔指定</option>
          </select>
        </div>

        {recurrenceType === RecurrenceType.INTERVAL && (
          <div className="mt-3">
            <label className="block text-sm text-gray-600">間隔（日数）</label>
            <input
              type="number"
              min={1}
              value={intervalDays}
              onChange={(e) => setIntervalDays(Number(e.target.value))}
              className="mt-1 block w-32 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
          </div>
        )}

        {recurrenceType === RecurrenceType.WEEKLY && (
          <div className="mt-3 flex flex-wrap gap-2">
            {ALL_WEEKDAYS.map((day) => (
              <label
                key={day.value}
                className="flex items-center gap-1 text-sm"
              >
                <input
                  type="checkbox"
                  checked={weekdays.includes(day.value)}
                  onChange={() => toggleWeekday(day.value)}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                {day.label}
              </label>
            ))}
          </div>
        )}
      </fieldset>

      <button
        type="submit"
        disabled={loading}
        className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
      >
        {loading
          ? "保存中..."
          : mode === "create"
            ? "登録"
            : "更新"}
      </button>
    </form>
  );
}
