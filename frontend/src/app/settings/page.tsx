"use client";

import { useEffect, useState } from "react";
import { getSettings, getTimezones } from "@/lib/api";
import SettingsForm from "@/components/SettingsForm";
import type { SettingsOut, TimezoneOption } from "@/lib/types";

export default function SettingsPage() {
  const [settings, setSettings] = useState<SettingsOut | null>(null);
  const [timezoneOptions, setTimezoneOptions] = useState<TimezoneOption[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getSettings(), getTimezones()])
      .then(([s, tz]) => {
        setSettings(s);
        setTimezoneOptions(tz);
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading || !settings) {
    return <p className="text-gray-500">読み込み中...</p>;
  }

  return (
    <div>
      <h1 className="mb-4 text-xl font-bold md:mb-6 md:text-2xl">設定</h1>
      <SettingsForm
        initialSettings={settings}
        timezoneOptions={timezoneOptions}
      />
    </div>
  );
}
