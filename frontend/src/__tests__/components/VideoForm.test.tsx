import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import VideoForm from "@/components/VideoForm";
import type { VideoOut, RecurrenceOut } from "@/lib/types";
import { RecurrenceType, DayOfWeek } from "@/lib/types";

const mockPush = vi.fn();
const mockRefresh = vi.fn();
vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: mockPush, refresh: mockRefresh }),
}));

const mockCreateVideo = vi.fn().mockResolvedValue({ id: "new-id" });
const mockUpdateVideo = vi.fn().mockResolvedValue({ id: "existing-id" });
const mockUpsertRecurrence = vi.fn().mockResolvedValue({});
const mockGetTags = vi.fn().mockResolvedValue([]);
vi.mock("@/lib/api", () => ({
  createVideo: (...args: unknown[]) => mockCreateVideo(...args),
  updateVideo: (...args: unknown[]) => mockUpdateVideo(...args),
  upsertRecurrence: (...args: unknown[]) => mockUpsertRecurrence(...args),
  getTags: (...args: unknown[]) => mockGetTags(...args),
}));

/** Find the input/textarea that is a sibling of a label with the given text */
function getFieldByLabel(labelText: string): HTMLInputElement | HTMLTextAreaElement {
  const label = screen.getByText(labelText, { selector: "label" });
  const container = label.parentElement!;
  const input = container.querySelector("input, textarea") as
    | HTMLInputElement
    | HTMLTextAreaElement;
  if (!input) throw new Error(`No input found for label "${labelText}"`);
  return input;
}

const initialData: VideoOut = {
  id: "existing-id",
  name: "Existing Video",
  url: "https://www.youtube.com/watch?v=xyz",
  comment: "existing comment",
  last_performed_date: null,
  next_scheduled_date: null,
  tags: [
    { id: "t1", name: "chest" },
    { id: "t2", name: "back" },
  ],
  created_at: "2026-01-01T00:00:00Z",
  updated_at: "2026-01-01T00:00:00Z",
};

const initialRecurrence: RecurrenceOut = {
  id: "r1",
  recurrence_type: RecurrenceType.WEEKLY,
  interval_days: null,
  weekdays: [DayOfWeek.MON, DayOfWeek.WED],
  created_at: "2026-01-01T00:00:00Z",
  updated_at: "2026-01-01T00:00:00Z",
};

beforeEach(() => {
  vi.clearAllMocks();
  mockGetTags.mockResolvedValue([]);
});

describe("create mode", () => {
  it("renders empty form", () => {
    render(<VideoForm mode="create" />);
    expect(getFieldByLabel("動画名")).toHaveValue("");
    expect(getFieldByLabel("URL")).toHaveValue("");
    expect(getFieldByLabel("コメント")).toHaveValue("");
    // TagInput should show no pills
    expect(screen.queryByLabelText(/を削除$/)).not.toBeInTheDocument();
  });

  it("calls createVideo on submit and navigates to /videos", async () => {
    const user = userEvent.setup();
    render(<VideoForm mode="create" />);

    await user.type(getFieldByLabel("動画名"), "New Video");
    await user.type(getFieldByLabel("URL"), "https://youtube.com/watch?v=1");
    await user.click(screen.getByRole("button", { name: "登録" }));

    await waitFor(() => {
      expect(mockCreateVideo).toHaveBeenCalledWith({
        name: "New Video",
        url: "https://youtube.com/watch?v=1",
        comment: null,
        next_scheduled_date: null,
        tag_names: [],
      });
      expect(mockPush).toHaveBeenCalledWith("/videos");
    });
  });

  it("submits selected tags via TagInput", async () => {
    mockGetTags.mockResolvedValue([
      { id: "t1", name: "chest" },
      { id: "t2", name: "arms" },
    ]);
    const user = userEvent.setup();
    render(<VideoForm mode="create" />);

    await user.type(getFieldByLabel("動画名"), "V");
    await user.type(getFieldByLabel("URL"), "https://youtube.com/watch?v=1");

    // Type in TagInput to search and select
    const tagInput = screen.getByLabelText("タグ入力");
    await user.type(tagInput, "ch");

    await waitFor(() => {
      expect(screen.getByText("chest")).toBeInTheDocument();
    });
    await user.click(screen.getByText("chest"));

    await user.click(screen.getByRole("button", { name: "登録" }));

    await waitFor(() => {
      expect(mockCreateVideo).toHaveBeenCalledWith(
        expect.objectContaining({ tag_names: ["chest"] })
      );
    });
  });
});

describe("edit mode", () => {
  it("pre-fills form with initialData", () => {
    render(
      <VideoForm
        mode="edit"
        initialData={initialData}
        initialRecurrence={initialRecurrence}
      />
    );
    expect(getFieldByLabel("動画名")).toHaveValue("Existing Video");
    expect(getFieldByLabel("URL")).toHaveValue(
      "https://www.youtube.com/watch?v=xyz"
    );
    expect(getFieldByLabel("コメント")).toHaveValue("existing comment");
    // Tags should be shown as pills
    expect(screen.getByText("chest")).toBeInTheDocument();
    expect(screen.getByText("back")).toBeInTheDocument();
  });

  it("calls updateVideo and navigates to /videos/{id}", async () => {
    const user = userEvent.setup();
    render(
      <VideoForm mode="edit" initialData={initialData} initialRecurrence={null} />
    );

    const nameInput = getFieldByLabel("動画名");
    await user.clear(nameInput);
    await user.type(nameInput, "Updated");
    await user.click(screen.getByRole("button", { name: "更新" }));

    await waitFor(() => {
      expect(mockUpdateVideo).toHaveBeenCalledWith(
        "existing-id",
        expect.objectContaining({ name: "Updated" })
      );
      expect(mockPush).toHaveBeenCalledWith("/videos/existing-id");
    });
  });
});

describe("recurrence settings", () => {
  it("shows interval days input when INTERVAL selected", async () => {
    const user = userEvent.setup();
    render(<VideoForm mode="create" />);

    await user.selectOptions(
      screen.getByRole("combobox"),
      RecurrenceType.INTERVAL
    );
    expect(getFieldByLabel("間隔（日数）")).toBeInTheDocument();
  });

  it("shows weekday checkboxes when WEEKLY selected", async () => {
    const user = userEvent.setup();
    render(<VideoForm mode="create" />);

    await user.selectOptions(
      screen.getByRole("combobox"),
      RecurrenceType.WEEKLY
    );
    expect(screen.getByLabelText("月")).toBeInTheDocument();
    expect(screen.getByLabelText("日")).toBeInTheDocument();
  });

  it("toggles weekday selection", async () => {
    const user = userEvent.setup();
    render(<VideoForm mode="create" />);

    await user.selectOptions(
      screen.getByRole("combobox"),
      RecurrenceType.WEEKLY
    );

    const monCheckbox = screen.getByLabelText("月");
    await user.click(monCheckbox);
    expect(monCheckbox).toBeChecked();

    await user.click(monCheckbox);
    expect(monCheckbox).not.toBeChecked();
  });

  it("does not call upsertRecurrence when type is NONE", async () => {
    const user = userEvent.setup();
    render(<VideoForm mode="create" />);

    await user.type(getFieldByLabel("動画名"), "V");
    await user.type(getFieldByLabel("URL"), "https://youtube.com/watch?v=1");
    await user.click(screen.getByRole("button", { name: "登録" }));

    await waitFor(() => {
      expect(mockCreateVideo).toHaveBeenCalled();
      expect(mockUpsertRecurrence).not.toHaveBeenCalled();
    });
  });
});

describe("loading and error", () => {
  it("disables submit button while loading", async () => {
    let resolvePromise: (value: unknown) => void;
    mockCreateVideo.mockReturnValue(
      new Promise((resolve) => {
        resolvePromise = resolve;
      })
    );

    const user = userEvent.setup();
    render(<VideoForm mode="create" />);

    await user.type(getFieldByLabel("動画名"), "V");
    await user.type(getFieldByLabel("URL"), "https://youtube.com/watch?v=1");
    await user.click(screen.getByRole("button", { name: "登録" }));

    expect(screen.getByRole("button", { name: "保存中..." })).toBeDisabled();

    resolvePromise!({ id: "x" });
  });

  it("shows alert on API error", async () => {
    mockCreateVideo.mockRejectedValue(new Error("API error 500: fail"));
    const alertSpy = vi.spyOn(window, "alert").mockImplementation(() => {});

    const user = userEvent.setup();
    render(<VideoForm mode="create" />);

    await user.type(getFieldByLabel("動画名"), "V");
    await user.type(getFieldByLabel("URL"), "https://youtube.com/watch?v=1");
    await user.click(screen.getByRole("button", { name: "登録" }));

    await waitFor(() => {
      expect(alertSpy).toHaveBeenCalledWith("API error 500: fail");
    });
  });
});
