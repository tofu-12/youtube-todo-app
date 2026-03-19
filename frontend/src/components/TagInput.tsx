"use client";

import { useState, useEffect, useRef } from "react";
import type { TagOut } from "@/lib/types";
import { getTags } from "@/lib/api";

interface TagInputProps {
  selectedTags: TagOut[];
  onChange: (tags: TagOut[]) => void;
}

export default function TagInput({ selectedTags, onChange }: TagInputProps) {
  const [allTags, setAllTags] = useState<TagOut[]>([]);
  const [query, setQuery] = useState("");
  const [isOpen, setIsOpen] = useState(false);
  const [highlightIndex, setHighlightIndex] = useState(0);
  const containerRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    getTags().then(setAllTags).catch(() => {});
  }, []);

  useEffect(() => {
    function handleMouseDown(e: MouseEvent) {
      if (
        containerRef.current &&
        !containerRef.current.contains(e.target as Node)
      ) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleMouseDown);
    return () => document.removeEventListener("mousedown", handleMouseDown);
  }, []);

  const selectedNames = new Set(selectedTags.map((t) => t.name.toLowerCase()));

  const filtered = allTags.filter(
    (t) =>
      !selectedNames.has(t.name.toLowerCase()) &&
      t.name.toLowerCase().includes(query.toLowerCase())
  );

  const trimmedQuery = query.trim();
  const exactMatch = allTags.some(
    (t) => t.name.toLowerCase() === trimmedQuery.toLowerCase()
  );
  const showCreate =
    trimmedQuery.length > 0 &&
    !exactMatch &&
    !selectedNames.has(trimmedQuery.toLowerCase());

  const options = [
    ...filtered,
    ...(showCreate
      ? [{ id: "", name: trimmedQuery, _isNew: true } as TagOut & { _isNew: boolean }]
      : []),
  ];

  useEffect(() => {
    setHighlightIndex(0);
  }, [query]);

  function addTag(tag: TagOut) {
    if (!selectedNames.has(tag.name.toLowerCase())) {
      onChange([...selectedTags, { id: tag.id, name: tag.name }]);
    }
    setQuery("");
    setIsOpen(false);
    inputRef.current?.focus();
  }

  function removeTag(index: number) {
    onChange(selectedTags.filter((_, i) => i !== index));
    inputRef.current?.focus();
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === "Enter") {
      e.preventDefault();
      if (isOpen && options.length > 0) {
        addTag(options[highlightIndex] ?? options[0]);
      }
    } else if (e.key === "ArrowDown") {
      e.preventDefault();
      setIsOpen(true);
      setHighlightIndex((prev) => Math.min(prev + 1, options.length - 1));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setHighlightIndex((prev) => Math.max(prev - 1, 0));
    } else if (e.key === "Backspace" && query === "") {
      if (selectedTags.length > 0) {
        removeTag(selectedTags.length - 1);
      }
    } else if (e.key === "Escape") {
      setIsOpen(false);
    }
  }

  return (
    <div ref={containerRef} className="relative">
      <div className="flex flex-wrap items-center gap-1 rounded-md border border-gray-300 bg-white px-2 py-1 shadow-sm focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-500">
        {selectedTags.map((tag, i) => (
          <span
            key={tag.id || tag.name}
            className="inline-flex items-center gap-1 rounded bg-blue-100 px-2 py-0.5 text-sm text-blue-800"
          >
            {tag.name}
            <button
              type="button"
              onClick={() => removeTag(i)}
              className="text-blue-600 hover:text-blue-900"
              aria-label={`${tag.name}を削除`}
            >
              ×
            </button>
          </span>
        ))}
        <input
          ref={inputRef}
          type="text"
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setIsOpen(true);
          }}
          onFocus={() => setIsOpen(true)}
          onKeyDown={handleKeyDown}
          placeholder={selectedTags.length === 0 ? "タグを入力..." : ""}
          className="min-w-[120px] flex-1 border-none p-1 text-sm outline-none focus:ring-0"
          aria-label="タグ入力"
        />
      </div>

      {isOpen && options.length > 0 && (
        <ul className="absolute z-10 mt-1 max-h-48 w-full overflow-auto rounded-md border border-gray-200 bg-white shadow-lg">
          {options.map((option, i) => {
            const isNew = "_isNew" in option && option._isNew;
            return (
              <li
                key={option.id || `new-${option.name}`}
                onMouseDown={(e) => e.preventDefault()}
                onClick={() => addTag(option)}
                className={`cursor-pointer px-3 py-2 text-sm ${
                  i === highlightIndex
                    ? "bg-blue-100 text-blue-900"
                    : "text-gray-700 hover:bg-gray-100"
                }`}
              >
                {isNew ? `「${option.name}」を新規作成` : option.name}
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}
