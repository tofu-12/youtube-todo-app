"use client";

import { useEffect, useState } from "react";
import { getAllVideos, getWorkoutHistories } from "@/lib/api";
import ScheduleCalendar from "@/components/ScheduleCalendar";
import type { CalendarEvent, CalendarFilterType } from "@/lib/types";

const FILTER_OPTIONS: { value: CalendarFilterType; label: string }[] = [
  { value: "all", label: "すべて" },
  { value: "scheduled", label: "予定" },
  { value: "performed", label: "実施済み" },
];

export default function CalendarPage() {
  const [events, setEvents] = useState<Map<string, CalendarEvent[]>>(
    new Map()
  );
  const [filter, setFilter] = useState<CalendarFilterType>("all");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      getAllVideos(),
      getWorkoutHistories("1970-01-01"),
    ])
      .then(([videos, histories]) => {
        const videoNameMap = new Map(
          videos.map((v) => [v.id, v.name])
        );
        const eventMap = new Map<string, CalendarEvent[]>();

        const addEvent = (date: string, event: CalendarEvent) => {
          if (!eventMap.has(date)) eventMap.set(date, []);
          eventMap.get(date)!.push(event);
        };

        for (const video of videos) {
          if (video.next_scheduled_date) {
            addEvent(video.next_scheduled_date, {
              videoId: video.id,
              videoName: video.name,
              type: "scheduled",
            });
          }
        }

        for (const history of histories) {
          addEvent(history.performed_date, {
            videoId: history.video_id,
            videoName: videoNameMap.get(history.video_id) ?? "不明な動画",
            type: "performed",
          });
        }

        setEvents(eventMap);
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <p className="text-gray-500">読み込み中...</p>;
  }

  return (
    <div>
      <h1 className="mb-4 text-2xl font-bold text-gray-900">カレンダー</h1>

      <div className="flex gap-2 mb-4">
        {FILTER_OPTIONS.map(({ value, label }) => (
          <button
            key={value}
            type="button"
            onClick={() => setFilter(value)}
            className={`px-3 py-1 text-sm rounded ${
              filter === value
                ? "bg-gray-800 text-white"
                : "bg-gray-200 text-gray-700 hover:bg-gray-300"
            }`}
          >
            {label}
          </button>
        ))}
      </div>

      <div className="rounded-lg border bg-white p-4">
        <ScheduleCalendar events={events} filter={filter} />
      </div>
    </div>
  );
}
