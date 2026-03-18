import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import VideoDetailClient from "@/app/videos/[id]/VideoDetailClient";
import type { VideoOut, RecurrenceOut, WorkoutHistoryOut } from "@/lib/types";
import { RecurrenceType, DayOfWeek } from "@/lib/types";

const mockPush = vi.fn();
const mockRefresh = vi.fn();
vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: mockPush, refresh: mockRefresh }),
}));

const mockDeleteVideo = vi.fn().mockResolvedValue(undefined);
vi.mock("@/lib/api", () => ({
  deleteVideo: (...args: unknown[]) => mockDeleteVideo(...args),
  createVideo: vi.fn(),
  updateVideo: vi.fn(),
  upsertRecurrence: vi.fn(),
}));

const baseVideo: VideoOut = {
  id: "v1",
  name: "My Video",
  url: "https://www.youtube.com/watch?v=abc",
  comment: "video comment",
  last_performed_date: "2026-03-18",
  next_scheduled_date: "2026-03-20",
  tags: [{ id: "t1", name: "chest" }],
  created_at: "2026-01-01T00:00:00Z",
  updated_at: "2026-01-01T00:00:00Z",
};

const dailyRecurrence: RecurrenceOut = {
  id: "r1",
  recurrence_type: RecurrenceType.DAILY,
  interval_days: null,
  weekdays: [],
  created_at: "2026-01-01T00:00:00Z",
  updated_at: "2026-01-01T00:00:00Z",
};

const intervalRecurrence: RecurrenceOut = {
  ...dailyRecurrence,
  recurrence_type: RecurrenceType.INTERVAL,
  interval_days: 3,
};

const weeklyRecurrence: RecurrenceOut = {
  ...dailyRecurrence,
  recurrence_type: RecurrenceType.WEEKLY,
  weekdays: [DayOfWeek.MON, DayOfWeek.FRI],
};

const workoutHistories: WorkoutHistoryOut[] = [
  {
    id: "wh1",
    video_id: "v1",
    performed_date: "2026-03-18",
    performed_at: "2026-03-18T10:00:00Z",
    expires_date: "2026-03-25",
    created_at: "2026-03-18T10:00:00Z",
    updated_at: "2026-03-18T10:00:00Z",
  },
];

beforeEach(() => {
  vi.clearAllMocks();
});

describe("display mode", () => {
  it("shows video name, URL link, comment, tags, scheduled and performed dates", () => {
    render(
      <VideoDetailClient
        video={baseVideo}
        recurrence={null}
        workoutHistories={[]}
      />
    );

    expect(screen.getByText("My Video")).toBeInTheDocument();

    const urlLink = screen.getByRole("link", {
      name: "https://www.youtube.com/watch?v=abc",
    });
    expect(urlLink).toHaveAttribute("href", "https://www.youtube.com/watch?v=abc");
    expect(urlLink).toHaveAttribute("target", "_blank");

    expect(screen.getByText("video comment")).toBeInTheDocument();
    expect(screen.getByText("chest")).toBeInTheDocument();
    expect(screen.getByText("2026-03-20")).toBeInTheDocument();
    expect(screen.getByText("2026-03-18")).toBeInTheDocument();
  });

  it("shows 未設定/未実施 when dates are null", () => {
    const video = { ...baseVideo, next_scheduled_date: null, last_performed_date: null };
    render(
      <VideoDetailClient video={video} recurrence={null} workoutHistories={[]} />
    );
    expect(screen.getByText("未設定")).toBeInTheDocument();
    expect(screen.getByText("未実施")).toBeInTheDocument();
  });
});

describe("recurrence rule display", () => {
  it("does not show recurrence section when null", () => {
    render(
      <VideoDetailClient
        video={baseVideo}
        recurrence={null}
        workoutHistories={[]}
      />
    );
    expect(screen.queryByText("繰り返しルール")).not.toBeInTheDocument();
  });

  it("shows 毎日 for DAILY", () => {
    render(
      <VideoDetailClient
        video={baseVideo}
        recurrence={dailyRecurrence}
        workoutHistories={[]}
      />
    );
    expect(screen.getByText("毎日")).toBeInTheDocument();
  });

  it("shows interval days for INTERVAL", () => {
    render(
      <VideoDetailClient
        video={baseVideo}
        recurrence={intervalRecurrence}
        workoutHistories={[]}
      />
    );
    expect(screen.getByText("間隔指定（3日ごと）")).toBeInTheDocument();
  });

  it("shows weekdays for WEEKLY", () => {
    render(
      <VideoDetailClient
        video={baseVideo}
        recurrence={weeklyRecurrence}
        workoutHistories={[]}
      />
    );
    expect(screen.getByText("毎週（mon, fri）")).toBeInTheDocument();
  });
});

describe("workout histories", () => {
  it("shows message when no histories", () => {
    render(
      <VideoDetailClient
        video={baseVideo}
        recurrence={null}
        workoutHistories={[]}
      />
    );
    expect(screen.getByText("履歴がありません")).toBeInTheDocument();
  });

  it("shows history dates when present", () => {
    render(
      <VideoDetailClient
        video={baseVideo}
        recurrence={null}
        workoutHistories={workoutHistories}
      />
    );
    expect(
      screen.getByText("2026-03-18（有効期限: 2026-03-25）")
    ).toBeInTheDocument();
  });
});

describe("edit mode", () => {
  it("shows VideoForm when edit button clicked", async () => {
    const user = userEvent.setup();
    render(
      <VideoDetailClient
        video={baseVideo}
        recurrence={null}
        workoutHistories={[]}
      />
    );

    await user.click(screen.getByRole("button", { name: "編集" }));
    expect(screen.getByText("動画編集")).toBeInTheDocument();
    // VideoForm is rendered; verify name input has the video name
    const label = screen.getByText("動画名", { selector: "label" });
    const nameInput = label.parentElement!.querySelector("input") as HTMLInputElement;
    expect(nameInput).toHaveValue("My Video");
  });
});

describe("delete", () => {
  it("calls deleteVideo and navigates when confirmed", async () => {
    vi.spyOn(window, "confirm").mockReturnValue(true);
    const user = userEvent.setup();

    render(
      <VideoDetailClient
        video={baseVideo}
        recurrence={null}
        workoutHistories={[]}
      />
    );

    await user.click(screen.getByRole("button", { name: "削除" }));

    await waitFor(() => {
      expect(mockDeleteVideo).toHaveBeenCalledWith("v1");
      expect(mockPush).toHaveBeenCalledWith("/videos");
    });
  });

  it("does nothing when confirm cancelled", async () => {
    vi.spyOn(window, "confirm").mockReturnValue(false);
    const user = userEvent.setup();

    render(
      <VideoDetailClient
        video={baseVideo}
        recurrence={null}
        workoutHistories={[]}
      />
    );

    await user.click(screen.getByRole("button", { name: "削除" }));

    expect(mockDeleteVideo).not.toHaveBeenCalled();
  });
});
