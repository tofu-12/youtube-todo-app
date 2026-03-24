import { render, screen, fireEvent } from "@testing-library/react";
import WorkoutCalendar from "@/components/WorkoutCalendar";

beforeEach(() => {
  vi.useFakeTimers();
  vi.setSystemTime(new Date(2026, 2, 25)); // 2026-03-25
});

afterEach(() => {
  vi.useRealTimers();
});

describe("WorkoutCalendar", () => {
  it("displays the current month by default", () => {
    render(<WorkoutCalendar performedDates={new Set()} />);
    expect(screen.getByText("2026年3月")).toBeInTheDocument();
  });

  it("highlights performed dates", () => {
    const dates = new Set(["2026-03-10", "2026-03-20"]);
    render(<WorkoutCalendar performedDates={dates} />);

    const day10 = screen.getByText("10");
    expect(day10.closest("div.bg-blue-600")).not.toBeNull();

    const day20 = screen.getByText("20");
    expect(day20.closest("div.bg-blue-600")).not.toBeNull();

    const day15 = screen.getByText("15");
    expect(day15.closest("div.bg-blue-600")).toBeNull();
  });

  it("highlights today with a ring", () => {
    render(<WorkoutCalendar performedDates={new Set()} />);

    const day25 = screen.getByText("25");
    expect(day25.closest("div.ring-1")).not.toBeNull();
  });

  it("navigates to the next month", () => {
    render(<WorkoutCalendar performedDates={new Set()} />);

    fireEvent.click(screen.getByRole("button", { name: "次月" }));
    expect(screen.getByText("2026年4月")).toBeInTheDocument();
  });

  it("navigates to the previous month", () => {
    render(<WorkoutCalendar performedDates={new Set()} />);

    fireEvent.click(screen.getByRole("button", { name: "前月" }));
    expect(screen.getByText("2026年2月")).toBeInTheDocument();
  });

  it("wraps year when navigating past December", () => {
    render(<WorkoutCalendar performedDates={new Set()} />);

    const nextButton = screen.getByRole("button", { name: "次月" });
    for (let i = 0; i < 10; i++) {
      fireEvent.click(nextButton);
    }
    expect(screen.getByText("2027年1月")).toBeInTheDocument();
  });

  it("wraps year when navigating before January", () => {
    render(<WorkoutCalendar performedDates={new Set()} />);

    const prevButton = screen.getByRole("button", { name: "前月" });
    for (let i = 0; i < 3; i++) {
      fireEvent.click(prevButton);
    }
    expect(screen.getByText("2025年12月")).toBeInTheDocument();
  });

  it("renders correct number of day cells for March 2026 (31 days)", () => {
    render(<WorkoutCalendar performedDates={new Set()} />);
    expect(screen.getByText("31")).toBeInTheDocument();
    expect(screen.queryByText("32")).not.toBeInTheDocument();
  });
});
