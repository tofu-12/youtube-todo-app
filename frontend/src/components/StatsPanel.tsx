"use client";

import { useEffect, useState, useCallback } from "react";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { getTodoHistoryStats, getTags } from "@/lib/api";
import type { TodoHistoryStats, StatsPeriod, TagOut } from "@/lib/types";

import type { PieLabelRenderProps } from "recharts";

const COLORS = { completed: "#22c55e", skipped: "#9ca3af" };

function renderInnerLabel(props: PieLabelRenderProps) {
  const { cx, cy, midAngle, innerRadius, outerRadius, value } = props;
  if (
    !value ||
    cx == null ||
    cy == null ||
    midAngle == null ||
    outerRadius == null
  )
    return null;
  const RADIAN = Math.PI / 180;
  const r = Number(innerRadius ?? 0);
  const R = Number(outerRadius);
  const radius = r + (R - r) * 0.5;
  const x = Number(cx) + radius * Math.cos(-Number(midAngle) * RADIAN);
  const y = Number(cy) + radius * Math.sin(-Number(midAngle) * RADIAN);
  return (
    <text
      x={x}
      y={y}
      fill="white"
      textAnchor="middle"
      dominantBaseline="central"
      fontSize={14}
      fontWeight="bold"
    >
      {value}
    </text>
  );
}

const PERIOD_OPTIONS: { value: StatsPeriod; label: string }[] = [
  { value: "last_7_days", label: "7日" },
  { value: "last_30_days", label: "30日" },
  { value: "last_90_days", label: "90日" },
];

export default function StatsPanel() {
  const [period, setPeriod] = useState<StatsPeriod>("last_90_days");
  const [tagId, setTagId] = useState("");
  const [stats, setStats] = useState<TodoHistoryStats | null>(null);
  const [tags, setTags] = useState<TagOut[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      try {
        const t = await getTags();
        setTags(t);
      } catch {
        // ignore
      }
    })();
  }, []);

  const fetchStats = useCallback(async () => {
    setLoading(true);
    try {
      const data = await getTodoHistoryStats(
        period,
        tagId || undefined
      );
      setStats(data);
    } catch {
      // ignore
    } finally {
      setLoading(false);
    }
  }, [period, tagId]);

  useEffect(() => {
    fetchStats();
  }, [fetchStats]);

  const chartData =
    stats && stats.total_count > 0
      ? [
          { name: "完了", value: stats.completed_count },
          { name: "スキップ", value: stats.skipped_count },
        ]
      : [];

  return (
    <div className="mb-4 rounded-lg border bg-white p-4 shadow-sm md:mb-6">
      <h2 className="mb-3 text-sm font-semibold text-gray-800">TODO達成率</h2>

      {/* Filters */}
      <div className="mb-3 flex items-center gap-3">
        <select
          value={period}
          onChange={(e) => setPeriod(e.target.value as StatsPeriod)}
          className="w-full max-w-28 rounded border border-gray-300 px-2 py-2 text-sm"
        >
          {PERIOD_OPTIONS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
        <select
          value={tagId}
          onChange={(e) => setTagId(e.target.value)}
          className="w-full max-w-36 rounded border border-gray-300 px-2 py-2 text-sm"
        >
          <option value="">すべてのタグ</option>
          {tags.map((tag) => (
            <option key={tag.id} value={tag.id}>
              {tag.name}
            </option>
          ))}
        </select>
      </div>

      {/* Chart + Summary */}
      {loading ? (
        <p className="text-sm text-gray-500">読み込み中...</p>
      ) : !stats || stats.total_count === 0 ? (
        <p className="text-sm text-gray-500">データがありません</p>
      ) : (
        <div style={{ height: 220 }}>
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={chartData}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                innerRadius={50}
                outerRadius={80}
                startAngle={90}
                endAngle={-270}
                label={renderInnerLabel}
                labelLine={false}
              >
                <Cell fill={COLORS.completed} />
                <Cell fill={COLORS.skipped} />
              </Pie>
              <Tooltip />
              <Legend />
              <text
                x="50%"
                y="45%"
                textAnchor="middle"
                dominantBaseline="central"
                className="fill-gray-800 text-2xl font-bold"
              >
                {stats.completion_rate}%
              </text>
            </PieChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}
