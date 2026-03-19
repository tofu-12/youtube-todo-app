"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import type { SettingsOut, TimezoneOption } from "@/lib/types";
import { updateSettings } from "@/lib/api";

interface SettingsFormProps {
  initialSettings: SettingsOut;
  timezoneOptions: TimezoneOption[];
}

export default function SettingsForm({
  initialSettings,
  timezoneOptions,
}: SettingsFormProps) {
  const router = useRouter();
  const [timezone, setTimezone] = useState(initialSettings.timezone);
  const [dayChangeTime, setDayChangeTime] = useState(
    initialSettings.day_change_time.slice(0, 5)
  );
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await updateSettings({
        timezone,
        day_change_time: dayChangeTime,
      });
      router.refresh();
      alert("設定を保存しました");
    } catch (err) {
      alert(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700">
          タイムゾーン
        </label>
        <select
          value={timezone}
          onChange={(e) => setTimezone(e.target.value)}
          className="mt-1 block w-full rounded border-gray-300 shadow-sm"
        >
          {timezoneOptions.map((tz) => (
            <option key={tz.value} value={tz.value}>
              {tz.label}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">
          日付変更時刻
        </label>
        <input
          type="time"
          value={dayChangeTime}
          onChange={(e) => setDayChangeTime(e.target.value)}
          className="mt-1 block w-full rounded border-gray-300 shadow-sm"
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? "保存中..." : "保存"}
      </button>
    </form>
  );
}
