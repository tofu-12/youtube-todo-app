"use client";

import { useState, useMemo } from "react";
import {
  WEEKDAY_LABELS,
  generateCalendarCells,
  formatDateString,
} from "@/lib/calendarUtils";
import type { CalendarEvent, CalendarFilterType } from "@/lib/types";

interface ScheduleCalendarProps {
  events: Map<string, CalendarEvent[]>;
  filter: CalendarFilterType;
}

export default function ScheduleCalendar({
  events,
  filter,
}: ScheduleCalendarProps) {
  const today = new Date();
  const [currentYear, setCurrentYear] = useState(today.getFullYear());
  const [currentMonth, setCurrentMonth] = useState(today.getMonth() + 1);

  const todayStr = formatDateString(
    today.getFullYear(),
    today.getMonth() + 1,
    today.getDate()
  );

  const filteredEvents = useMemo(() => {
    if (filter === "all") return events;
    const filtered = new Map<string, CalendarEvent[]>();
    for (const [date, dayEvents] of events) {
      const matching = dayEvents.filter((e) => e.type === filter);
      if (matching.length > 0) {
        filtered.set(date, matching);
      }
    }
    return filtered;
  }, [events, filter]);

  const goToPreviousMonth = () => {
    if (currentMonth === 1) {
      setCurrentYear((y) => y - 1);
      setCurrentMonth(12);
    } else {
      setCurrentMonth((m) => m - 1);
    }
  };

  const goToNextMonth = () => {
    if (currentMonth === 12) {
      setCurrentYear((y) => y + 1);
      setCurrentMonth(1);
    } else {
      setCurrentMonth((m) => m + 1);
    }
  };

  const cells = generateCalendarCells(currentYear, currentMonth);

  return (
    <div>
      <div className="flex items-center justify-between mb-3">
        <button
          type="button"
          onClick={goToPreviousMonth}
          className="text-gray-500 hover:text-gray-700 text-sm px-3 py-2 md:px-2 md:py-1"
          aria-label="前月"
        >
          &lt;
        </button>
        <span className="text-sm font-medium text-gray-900">
          {currentYear}年{currentMonth}月
        </span>
        <button
          type="button"
          onClick={goToNextMonth}
          className="text-gray-500 hover:text-gray-700 text-sm px-3 py-2 md:px-2 md:py-1"
          aria-label="次月"
        >
          &gt;
        </button>
      </div>

      <div className="overflow-x-auto">
        <div className="min-w-[500px]">
      <div className="grid grid-cols-7 text-center text-xs text-gray-500 mb-1">
        {WEEKDAY_LABELS.map((label) => (
          <div key={label} className="py-1 font-medium">
            {label}
          </div>
        ))}
      </div>

      <div className="grid grid-cols-7 border-t border-l">
        {cells.map((day, index) => {
          if (day === null) {
            return (
              <div
                key={`empty-${index}`}
                className="min-h-[60px] border-r border-b bg-gray-50 md:min-h-[80px]"
              />
            );
          }

          const dateStr = formatDateString(currentYear, currentMonth, day);
          const isToday = dateStr === todayStr;
          const dayEvents = filteredEvents.get(dateStr) ?? [];

          return (
            <div
              key={day}
              className="min-h-[60px] border-r border-b p-1 bg-white md:min-h-[80px]"
            >
              <div className="flex justify-start mb-0.5">
                <span
                  className={`text-xs w-6 h-6 flex items-center justify-center ${
                    isToday
                      ? "bg-blue-600 text-white rounded-full font-medium"
                      : "text-gray-700"
                  }`}
                >
                  {day}
                </span>
              </div>
              <div className="space-y-0.5">
                {dayEvents.map((event, i) => (
                  <div
                    key={`${event.videoId}-${event.type}-${i}`}
                    className={`text-xs px-1 py-0.5 rounded truncate border-l-2 ${
                      event.type === "scheduled"
                        ? "bg-blue-50 text-blue-800 border-blue-500"
                        : "bg-green-50 text-green-800 border-green-500"
                    }`}
                    title={event.videoName}
                  >
                    {event.videoName}
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>
        </div>
      </div>
    </div>
  );
}
