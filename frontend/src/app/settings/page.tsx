import { getSettings, getTimezones } from "@/lib/api";
import SettingsForm from "@/components/SettingsForm";

export default async function SettingsPage() {
  const [settings, timezoneOptions] = await Promise.all([
    getSettings(),
    getTimezones(),
  ]);

  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold">設定</h1>
      <SettingsForm
        initialSettings={settings}
        timezoneOptions={timezoneOptions}
      />
    </div>
  );
}
