"use client";

import { useEffect, useState, useCallback, useRef } from "react";
import Link from "next/link";
import { getVideos, getTags } from "@/lib/api";
import VideoForm from "@/components/VideoForm";
import type { VideoOut, TagOut } from "@/lib/types";
import {
  ScheduledStatus,
  VideoSortField,
  SortOrder,
} from "@/lib/types";

const SCHEDULED_STATUS_LABELS: Record<string, string> = {
  "": "すべて",
  [ScheduledStatus.OVERDUE]: "期限切れ",
  [ScheduledStatus.TODAY]: "今日",
  [ScheduledStatus.UPCOMING]: "予定あり",
  [ScheduledStatus.UNSCHEDULED]: "未設定",
};

const SORT_FIELD_LABELS: Record<string, string> = {
  [VideoSortField.CREATED_AT]: "登録日時",
  [VideoSortField.NAME]: "動画名",
  [VideoSortField.UPDATED_AT]: "更新日時",
  [VideoSortField.NEXT_SCHEDULED_DATE]: "次回予定日",
  [VideoSortField.LAST_PERFORMED_DATE]: "最終実施日",
};

const PAGE_SIZE = 20;

export default function VideosPage() {
  const [videos, setVideos] = useState<VideoOut[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);

  // Filters
  const [nameQuery, setNameQuery] = useState("");
  const [debouncedName, setDebouncedName] = useState("");
  const [selectedTagNames, setSelectedTagNames] = useState<string[]>([]);
  const [scheduledStatus, setScheduledStatus] = useState<string>("");

  // Sort
  const [sortField, setSortField] = useState<VideoSortField>(VideoSortField.CREATED_AT);
  const [sortOrder, setSortOrder] = useState<SortOrder>(SortOrder.DESC);

  // Pagination
  const [page, setPage] = useState(0);

  // Registration modal
  const [showNewForm, setShowNewForm] = useState(false);
  const [formKey, setFormKey] = useState(0);

  // Tags for filter
  const [allTags, setAllTags] = useState<TagOut[]>([]);

  useEffect(() => {
    getTags().then(setAllTags).catch(() => {});
  }, []);

  // Debounce name search
  const debounceRef = useRef<ReturnType<typeof setTimeout>>(undefined);
  useEffect(() => {
    debounceRef.current = setTimeout(() => {
      setDebouncedName(nameQuery);
      setPage(0);
    }, 300);
    return () => clearTimeout(debounceRef.current);
  }, [nameQuery]);

  const fetchVideos = useCallback(async () => {
    setLoading(true);
    try {
      const data = await getVideos({
        name: debouncedName || undefined,
        tag_names: selectedTagNames.length > 0 ? selectedTagNames : undefined,
        scheduled_status: scheduledStatus ? (scheduledStatus as ScheduledStatus) : undefined,
        sort_field: sortField,
        sort_order: sortOrder,
        skip: page * PAGE_SIZE,
        limit: PAGE_SIZE,
      });
      setVideos(data.items);
      setTotal(data.total);
    } catch {
      // Error handled silently
    } finally {
      setLoading(false);
    }
  }, [debouncedName, selectedTagNames, scheduledStatus, sortField, sortOrder, page]);

  useEffect(() => {
    fetchVideos();
  }, [fetchVideos]);

  const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE));

  function handleTagToggle(tagName: string) {
    setSelectedTagNames((prev) =>
      prev.includes(tagName)
        ? prev.filter((t) => t !== tagName)
        : [...prev, tagName]
    );
    setPage(0);
  }

  function handleStatusChange(value: string) {
    setScheduledStatus(value);
    setPage(0);
  }

  function handleSortFieldChange(value: string) {
    setSortField(value as VideoSortField);
    setPage(0);
  }

  function handleSortOrderToggle() {
    setSortOrder((prev) => (prev === SortOrder.DESC ? SortOrder.ASC : SortOrder.DESC));
    setPage(0);
  }

  function handleCreateSuccess() {
    setShowNewForm(false);
    fetchVideos();
  }

  function openNewForm() {
    setFormKey((k) => k + 1);
    setShowNewForm(true);
  }

  useEffect(() => {
    if (showNewForm) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }
    return () => {
      document.body.style.overflow = "";
    };
  }, [showNewForm]);

  return (
    <div>
      <div className="mb-4 flex items-center justify-between md:mb-6">
        <h1 className="text-xl font-bold text-gray-900 md:text-2xl">動画一覧</h1>
        <button
          type="button"
          onClick={openNewForm}
          className="rounded-md bg-blue-600 px-4 py-2.5 text-sm font-medium text-white hover:bg-blue-700 md:px-3 md:py-1.5"
        >
          + 動画登録
        </button>
      </div>

      {/* Filters */}
      <div className="mb-4 space-y-3">
        {/* Search */}
        <input
          type="text"
          value={nameQuery}
          onChange={(e) => setNameQuery(e.target.value)}
          placeholder="動画名で検索..."
          className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
        />

        {/* Tag filter + Status filter row */}
        <div className="flex flex-col gap-3 sm:flex-row sm:flex-wrap sm:items-center">
          {/* Status filter */}
          <select
            value={scheduledStatus}
            onChange={(e) => handleStatusChange(e.target.value)}
            className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 sm:w-auto md:py-1.5"
          >
            {Object.entries(SCHEDULED_STATUS_LABELS).map(([value, label]) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </select>

          {/* Sort controls */}
          <select
            value={sortField}
            onChange={(e) => handleSortFieldChange(e.target.value)}
            className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 sm:w-auto md:py-1.5"
          >
            {Object.entries(SORT_FIELD_LABELS).map(([value, label]) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </select>

          <button
            type="button"
            onClick={handleSortOrderToggle}
            className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm hover:bg-gray-50 sm:w-auto md:py-1.5"
            title={sortOrder === SortOrder.DESC ? "降順" : "昇順"}
          >
            {sortOrder === SortOrder.DESC ? "↓ 降順" : "↑ 昇順"}
          </button>
        </div>

        {/* Tag filter chips */}
        {allTags.length > 0 && (
          <div className="flex flex-wrap gap-1">
            {allTags.map((tag) => {
              const selected = selectedTagNames.includes(tag.name);
              return (
                <button
                  key={tag.id}
                  type="button"
                  onClick={() => handleTagToggle(tag.name)}
                  className={`rounded-full px-3 py-1.5 text-sm transition-colors md:px-2.5 md:py-0.5 md:text-xs ${
                    selected
                      ? "bg-blue-600 text-white"
                      : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                  }`}
                >
                  {tag.name}
                </button>
              );
            })}
          </div>
        )}
      </div>

      {/* Results info */}
      <div className="mb-3 text-sm text-gray-500">
        {total > 0
          ? `全${total}件中 ${page * PAGE_SIZE + 1}〜${Math.min((page + 1) * PAGE_SIZE, total)}件表示`
          : "0件"}
      </div>

      {/* Video list */}
      {loading ? (
        <p className="text-gray-500">読み込み中...</p>
      ) : videos.length === 0 ? (
        <p className="text-gray-500">
          {debouncedName || selectedTagNames.length > 0 || scheduledStatus
            ? "条件に一致する動画がありません。"
            : (
                <>
                  動画が登録されていません。
                  <button type="button" onClick={openNewForm} className="text-blue-600 hover:underline">
                    動画を登録
                  </button>
                  してください。
                </>
              )}
        </p>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2">
          {videos.map((video) => (
            <Link
              key={video.id}
              href={`/videos/${video.id}`}
              className="block rounded-lg border bg-white p-4 shadow-sm hover:shadow-md transition-shadow"
            >
              <h2 className="font-semibold text-gray-900">{video.name}</h2>
              {video.tags.length > 0 && (
                <div className="mt-1 flex flex-wrap gap-1">
                  {video.tags.map((tag) => (
                    <span
                      key={tag.id}
                      className="inline-block rounded-full bg-blue-100 px-2 py-0.5 text-xs text-blue-800"
                    >
                      {tag.name}
                    </span>
                  ))}
                </div>
              )}
              <div className="mt-2 space-y-0.5 text-sm text-gray-500">
                {video.next_scheduled_date && (
                  <p>次回予定: {video.next_scheduled_date}</p>
                )}
                <p>最終実施: {video.last_performed_date ?? "未実施"}</p>
              </div>
            </Link>
          ))}
        </div>
      )}

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="mt-6 flex items-center justify-center gap-4">
          <button
            type="button"
            onClick={() => setPage((p) => Math.max(0, p - 1))}
            disabled={page === 0}
            className="rounded-md border border-gray-300 px-4 py-2.5 text-sm shadow-sm hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-50 md:px-3 md:py-1.5"
          >
            ← 前へ
          </button>
          <span className="text-sm text-gray-600">
            {page + 1} / {totalPages} ページ
          </span>
          <button
            type="button"
            onClick={() => setPage((p) => Math.min(totalPages - 1, p + 1))}
            disabled={page >= totalPages - 1}
            className="rounded-md border border-gray-300 px-4 py-2.5 text-sm shadow-sm hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-50 md:px-3 md:py-1.5"
          >
            次へ →
          </button>
        </div>
      )}

      {/* Registration modal */}
      {showNewForm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
          <div className="relative mx-4 max-h-[90vh] w-full max-w-lg overflow-y-auto rounded-lg bg-white p-6 shadow-xl">
            <div className="mb-4 flex items-center justify-between">
              <h2 className="text-xl font-bold text-gray-900">動画登録</h2>
              <button
                type="button"
                onClick={() => setShowNewForm(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                ✕
              </button>
            </div>
            <VideoForm key={formKey} mode="create" onSuccess={handleCreateSuccess} />
          </div>
        </div>
      )}
    </div>
  );
}
