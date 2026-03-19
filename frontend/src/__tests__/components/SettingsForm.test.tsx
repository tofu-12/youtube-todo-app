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
    const select = screen.getByRole("combobox");
    expect(select).toHaveValue("Asia/Tokyo");
    expect(screen.getByDisplayValue("04:00")).toBeInTheDocument();
  });

  it("renders all timezone options", () => {
    render(
      <SettingsForm
        initialSettings={initialSettings}
        timezoneOptions={timezoneOptions}
      />
    );
    const options = screen.getAllByRole("option");
    expect(options).toHaveLength(3);
  });

  it("calls updateSettings on submit", async () => {
    const user = userEvent.setup();
    render(
      <SettingsForm
        initialSettings={initialSettings}
        timezoneOptions={timezoneOptions}
      />
    );

    await user.selectOptions(screen.getByRole("combobox"), "America/New_York");
    await user.click(screen.getByRole("button", { name: "保存" }));

    await waitFor(() => {
      expect(mockUpdateSettings).toHaveBeenCalledWith({
        timezone: "America/New_York",
        day_change_time: "04:00",
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
