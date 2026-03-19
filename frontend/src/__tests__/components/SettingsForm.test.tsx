import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import SettingsForm from "@/components/SettingsForm";
import type { SettingsOut, TimezoneOption } from "@/lib/types";

const mockRefresh = vi.fn();
vi.mock("next/navigation", () => ({
  useRouter: () => ({ refresh: mockRefresh }),
}));

const mockUpdateSettings = vi.fn().mockResolvedValue({
  day_change_time: "04:00:00",
  timezone: "Asia/Tokyo",
});
vi.mock("@/lib/api", () => ({
  updateSettings: (...args: unknown[]) => mockUpdateSettings(...args),
}));

const initialSettings: SettingsOut = {
  day_change_time: "04:00:00",
  timezone: "Asia/Tokyo",
  workout_history_expires_days: 90,
};

const timezoneOptions: TimezoneOption[] = [
  { value: "UTC", label: "UTC" },
  { value: "Asia/Tokyo", label: "Asia/Tokyo" },
  { value: "America/New_York", label: "America/New_York" },
];

beforeEach(() => {
  vi.clearAllMocks();
});

describe("SettingsForm", () => {
  it("renders with initial values", () => {
    render(
      <SettingsForm
        initialSettings={initialSettings}
        timezoneOptions={timezoneOptions}
      />
    );
    const selects = screen.getAllByRole("combobox");
    expect(selects[0]).toHaveValue("Asia/Tokyo");
    expect(screen.getByDisplayValue("04:00")).toBeInTheDocument();
    expect(selects[1]).toHaveValue("90");
  });

  it("renders all timezone options", () => {
    render(
      <SettingsForm
        initialSettings={initialSettings}
        timezoneOptions={timezoneOptions}
      />
    );
    const options = screen.getAllByRole("option");
    // 3 timezone options + 5 expires_days options
    expect(options).toHaveLength(8);
  });

  it("calls updateSettings on submit", async () => {
    const user = userEvent.setup();
    render(
      <SettingsForm
        initialSettings={initialSettings}
        timezoneOptions={timezoneOptions}
      />
    );

    const selects = screen.getAllByRole("combobox");
    await user.selectOptions(selects[0], "America/New_York");
    await user.click(screen.getByRole("button", { name: "保存" }));

    await waitFor(() => {
      expect(mockUpdateSettings).toHaveBeenCalledWith({
        timezone: "America/New_York",
        day_change_time: "04:00",
        workout_history_expires_days: 90,
      });
      expect(mockRefresh).toHaveBeenCalled();
    });
  });

  it("disables button while loading", async () => {
    let resolvePromise: (value: unknown) => void;
    mockUpdateSettings.mockReturnValue(
      new Promise((resolve) => {
        resolvePromise = resolve;
      })
    );

    const user = userEvent.setup();
    render(
      <SettingsForm
        initialSettings={initialSettings}
        timezoneOptions={timezoneOptions}
      />
    );

    await user.click(screen.getByRole("button", { name: "保存" }));

    expect(screen.getByRole("button", { name: "保存中..." })).toBeDisabled();

    resolvePromise!({ day_change_time: "04:00:00", timezone: "Asia/Tokyo" });
  });

  it("renders workout history expires days select", () => {
    render(
      <SettingsForm
        initialSettings={initialSettings}
        timezoneOptions={timezoneOptions}
      />
    );
    expect(
      screen.getByText("ワークアウト履歴の有効期限")
    ).toBeInTheDocument();
    const selects = screen.getAllByRole("combobox");
    const expiresSelect = selects[1];
    expect(expiresSelect).toHaveValue("90");
  });

  it("updates workout_history_expires_days on submit", async () => {
    const user = userEvent.setup();
    render(
      <SettingsForm
        initialSettings={initialSettings}
        timezoneOptions={timezoneOptions}
      />
    );

    const selects = screen.getAllByRole("combobox");
    await user.selectOptions(selects[1], "180");
    await user.click(screen.getByRole("button", { name: "保存" }));

    await waitFor(() => {
      expect(mockUpdateSettings).toHaveBeenCalledWith({
        timezone: "Asia/Tokyo",
        day_change_time: "04:00",
        workout_history_expires_days: 180,
      });
    });
  });

  it("shows alert on error", async () => {
    mockUpdateSettings.mockRejectedValue(new Error("API error 500: fail"));
    const alertSpy = vi.spyOn(window, "alert").mockImplementation(() => {});

    const user = userEvent.setup();
    render(
      <SettingsForm
        initialSettings={initialSettings}
        timezoneOptions={timezoneOptions}
      />
    );

    await user.click(screen.getByRole("button", { name: "保存" }));

    await waitFor(() => {
      expect(alertSpy).toHaveBeenCalledWith("API error 500: fail");
    });
  });
});
