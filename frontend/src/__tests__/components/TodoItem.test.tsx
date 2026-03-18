import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import TodoItem from "@/components/TodoItem";
import type { TodayVideoOut } from "@/lib/types";
import { TodoStatus } from "@/lib/types";

const mockRefresh = vi.fn();
vi.mock("next/navigation", () => ({
  useRouter: () => ({ refresh: mockRefresh }),
}));

const mockCreateTodoHistory = vi.fn().mockResolvedValue({});
const mockCreateWorkoutHistory = vi.fn().mockResolvedValue({});
vi.mock("@/lib/api", () => ({
  createTodoHistory: (...args: unknown[]) => mockCreateTodoHistory(...args),
  createWorkoutHistory: (...args: unknown[]) => mockCreateWorkoutHistory(...args),
}));

const baseVideo: TodayVideoOut = {
  id: "v1",
  name: "Test Video",
  url: "https://www.youtube.com/watch?v=abc",
  comment: "A test comment",
  next_scheduled_date: "2026-03-19",
  tags: [
    { id: "t1", name: "chest" },
    { id: "t2", name: "arms" },
  ],
};

beforeEach(() => {
  vi.clearAllMocks();
});

describe("TodoItem rendering", () => {
  it("displays video name, tags, date, comment, and YouTube link", () => {
    render(<TodoItem video={baseVideo} />);

    expect(screen.getByText("Test Video")).toBeInTheDocument();
    expect(screen.getByText("chest")).toBeInTheDocument();
    expect(screen.getByText("arms")).toBeInTheDocument();
    expect(screen.getByText("予定日: 2026-03-19")).toBeInTheDocument();
    expect(screen.getByText("A test comment")).toBeInTheDocument();

    const ytLink = screen.getByRole("link", { name: "YouTube" });
    expect(ytLink).toHaveAttribute("href", "https://www.youtube.com/watch?v=abc");
    expect(ytLink).toHaveAttribute("target", "_blank");

    expect(screen.getByRole("button", { name: "完了" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "スキップ" })).toBeInTheDocument();
  });
});

describe("complete button", () => {
  it("calls createTodoHistory(COMPLETED) + createWorkoutHistory then refreshes", async () => {
    const user = userEvent.setup();
    render(<TodoItem video={baseVideo} />);

    await user.click(screen.getByRole("button", { name: "完了" }));

    await waitFor(() => {
      expect(mockCreateTodoHistory).toHaveBeenCalledWith({
        video_id: "v1",
        scheduled_date: "2026-03-19",
        status: TodoStatus.COMPLETED,
      });
      expect(mockCreateWorkoutHistory).toHaveBeenCalledWith({
        video_id: "v1",
        expires_days: 7,
      });
      expect(mockRefresh).toHaveBeenCalled();
    });
  });
});

describe("skip button", () => {
  it("calls createTodoHistory(SKIPPED) only then refreshes", async () => {
    const user = userEvent.setup();
    render(<TodoItem video={baseVideo} />);

    await user.click(screen.getByRole("button", { name: "スキップ" }));

    await waitFor(() => {
      expect(mockCreateTodoHistory).toHaveBeenCalledWith({
        video_id: "v1",
        scheduled_date: "2026-03-19",
        status: TodoStatus.SKIPPED,
      });
      expect(mockCreateWorkoutHistory).not.toHaveBeenCalled();
      expect(mockRefresh).toHaveBeenCalled();
    });
  });
});

describe("loading state", () => {
  it("disables buttons during processing", async () => {
    let resolvePromise: (value: unknown) => void;
    mockCreateTodoHistory.mockReturnValue(
      new Promise((resolve) => {
        resolvePromise = resolve;
      })
    );

    const user = userEvent.setup();
    render(<TodoItem video={baseVideo} />);

    await user.click(screen.getByRole("button", { name: "完了" }));

    expect(screen.getByRole("button", { name: "完了" })).toBeDisabled();
    expect(screen.getByRole("button", { name: "スキップ" })).toBeDisabled();

    resolvePromise!({});
  });
});
