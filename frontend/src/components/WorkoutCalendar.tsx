"use client";

import { useState } from "react";
import {
  WEEKDAY_LABELS,
  generateCalendarCells,
  formatDateString,
} from "@/lib/calendarUtils";

interface WorkoutCalendarProps {
  performedDates: Set<string>;
}

export default function WorkoutCalendar({ performedDates }: WorkoutCalendarProps) {
  const today = new Date();
  const [currentYear, setCurrentYear] = useState(today.getFullYear());
  const [currentMonth, setCurrentMonth] = useState(today.getMonth() + 1);

  const todayStr = formatDateString(
    today.getFullYear(),
    today.getMonth() + 1,
    today.getDate()
  );

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
          className="text-gray-500 hover:text-gray-700 text-sm px-2 py-1"
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
          className="text-gray-500 hover:text-gray-700 text-sm px-2 py-1"
          aria-label="次月"
        >
          &gt;
        </button>
      </div>

      <div className="grid grid-cols-7 text-center text-xs text-gray-500 mb-1">
        {WEEKDAY_LABELS.map((label) => (
          <div key={label}>{label}</div>
        ))}
      </div>

      <div className="grid grid-cols-7 text-center text-sm">
        {cells.map((day, index) => {
          if (day === null) {
            return <div key={`empty-${index}`} className="py-1" />;
          }

          const dateStr = formatDateString(currentYear, currentMonth, day);
          const isPerformed = performedDates.has(dateStr);
          const isToday = dateStr === todayStr;

          let cellClass = "py-1 mx-auto w-7 h-7 flex items-center justify-center";
          if (isToday) {
            cellClass += " bg-blue-600 text-white rounded-full font-medium";
          } else if (isPerformed) {
            cellClass += " ring-2 ring-blue-500 rounded-full text-gray-700";
          } else {
            cellClass += " text-gray-700";
          }

          return (
            <div key={day} className="py-1">
              <div className={cellClass}>{day}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
