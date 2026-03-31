import type {
  AuthResponse,
  PaginatedVideoOut,
  RecurrenceOut,
  RecurrenceRequest,
  SettingsOut,
  SettingsUpdateRequest,
  StatsPeriod,
  TagOut,
  TimezoneOption,
  TodayVideoOut,
  TodoHistoryCreateRequest,
  TodoHistoryOut,
  TodoHistoryStats,
  VideoCreateRequest,
  VideoListParams,
  VideoOut,
  VideoUpdateRequest,
  WorkoutHistoryCreateRequest,
  WorkoutHistoryOut,
} from "./types";

const API_URL = "";

async function fetchApi<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const userId =
    typeof window !== "undefined"
      ? localStorage.getItem("user_id")
      : null;

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };

  if (userId) {
    headers["X-User-Id"] = userId;
  }

  const res = await fetch(`${API_URL}${path}`, {
    ...options,
    headers,
  });

  if (!res.ok) {
    if (res.status === 401 && typeof window !== "undefined") {
      localStorage.removeItem("user_id");
      localStorage.removeItem("user_email");
      window.location.replace("/auth");
      return new Promise<T>(() => {});
    }
    const body = await res.text();
    throw new Error(`API error ${res.status}: ${body}`);
  }

  if (res.status === 204) {
    return undefined as T;
  }

  return res.json() as Promise<T>;
}

// Tags

export async function getTags(): Promise<TagOut[]> {
  return fetchApi<TagOut[]>("/api/tags", { cache: "no-store" });
}

// Videos

export async function getVideos(
  params?: VideoListParams
): Promise<PaginatedVideoOut> {
  const query = new URLSearchParams();
  if (params?.name) query.set("name", params.name);
  if (params?.tag_names) {
    params.tag_names.forEach((t) => query.append("tag_names", t));
  }
  if (params?.scheduled_status) query.set("scheduled_status", params.scheduled_status);
  if (params?.sort_field) query.set("sort_field", params.sort_field);
  if (params?.sort_order) query.set("sort_order", params.sort_order);
  if (params?.skip !== undefined) query.set("skip", String(params.skip));
  if (params?.limit !== undefined) query.set("limit", String(params.limit));
  const qs = query.toString();
  return fetchApi<PaginatedVideoOut>(`/api/videos${qs ? `?${qs}` : ""}`, {
    cache: "no-store",
  });
}

export async function getAllVideos(): Promise<VideoOut[]> {
  return fetchApi<VideoOut[]>("/api/videos/all", { cache: "no-store" });
}

export async function getVideo(id: string): Promise<VideoOut> {
  return fetchApi<VideoOut>(`/api/videos/${id}`, { cache: "no-store" });
}

export async function createVideo(
  data: VideoCreateRequest
): Promise<VideoOut> {
  return fetchApi<VideoOut>("/api/videos", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function updateVideo(
  id: string,
  data: VideoUpdateRequest
): Promise<VideoOut> {
  return fetchApi<VideoOut>(`/api/videos/${id}`, {
    method: "PUT",
    body: JSON.stringify(data),
  });
}

export async function deleteVideo(id: string): Promise<void> {
  return fetchApi<void>(`/api/videos/${id}`, { method: "DELETE" });
}

// Recurrences

export async function getRecurrence(
  videoId: string
): Promise<RecurrenceOut | null> {
  try {
    return await fetchApi<RecurrenceOut>(
      `/api/videos/${videoId}/recurrence`,
      { cache: "no-store" }
    );
  } catch (e) {
    if (e instanceof Error && e.message.includes("404")) {
      return null;
    }
    throw e;
  }
}

export async function upsertRecurrence(
  videoId: string,
  data: RecurrenceRequest
): Promise<RecurrenceOut> {
  return fetchApi<RecurrenceOut>(`/api/videos/${videoId}/recurrence`, {
    method: "PUT",
    body: JSON.stringify(data),
  });
}

export async function deleteRecurrence(videoId: string): Promise<void> {
  return fetchApi<void>(`/api/videos/${videoId}/recurrence`, {
    method: "DELETE",
  });
}

// Today / Overdue

export async function getTodayVideos(): Promise<TodayVideoOut[]> {
  return fetchApi<TodayVideoOut[]>("/api/today", { cache: "no-store" });
}

export async function getOverdueVideos(): Promise<TodayVideoOut[]> {
  return fetchApi<TodayVideoOut[]>("/api/overdue", { cache: "no-store" });
}

// Todo Histories

export async function getTodoHistories(
  scheduledDate?: string
): Promise<TodoHistoryOut[]> {
  const query = scheduledDate
    ? `?scheduled_date=${scheduledDate}`
    : "";
  return fetchApi<TodoHistoryOut[]>(`/api/todo-histories${query}`, {
    cache: "no-store",
  });
}

export async function createTodoHistory(
  data: TodoHistoryCreateRequest
): Promise<TodoHistoryOut> {
  return fetchApi<TodoHistoryOut>("/api/todo-histories", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function deleteTodoHistory(id: string): Promise<void> {
  return fetchApi<void>(`/api/todo-histories/${id}`, { method: "DELETE" });
}

export async function getTodoHistoryStats(
  period: StatsPeriod = "last_90_days",
  tagId?: string
): Promise<TodoHistoryStats> {
  const query = new URLSearchParams();
  query.set("period", period);
  if (tagId) query.set("tag_id", tagId);
  return fetchApi<TodoHistoryStats>(
    `/api/todo-histories/stats?${query.toString()}`,
    { cache: "no-store" }
  );
}

// Workout Histories

export async function getWorkoutHistories(
  expiresAfter?: string
): Promise<WorkoutHistoryOut[]> {
  const query = expiresAfter ? `?expires_after=${expiresAfter}` : "";
  return fetchApi<WorkoutHistoryOut[]>(`/api/workout-histories${query}`, {
    cache: "no-store",
  });
}

export async function createWorkoutHistory(
  data: WorkoutHistoryCreateRequest
): Promise<WorkoutHistoryOut> {
  return fetchApi<WorkoutHistoryOut>("/api/workout-histories", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function deleteWorkoutHistory(id: string): Promise<void> {
  return fetchApi<void>(`/api/workout-histories/${id}`, {
    method: "DELETE",
  });
}

// Settings

export async function getTimezones(): Promise<TimezoneOption[]> {
  return fetchApi<TimezoneOption[]>("/api/settings/timezones", {
    cache: "no-store",
  });
}

export async function getSettings(): Promise<SettingsOut> {
  return fetchApi<SettingsOut>("/api/settings", { cache: "no-store" });
}

export async function updateSettings(
  data: SettingsUpdateRequest
): Promise<SettingsOut> {
  return fetchApi<SettingsOut>("/api/settings", {
    method: "PUT",
    body: JSON.stringify(data),
  });
}

// Auth

export async function loginUser(email: string): Promise<AuthResponse> {
  return fetchApi<AuthResponse>("/api/auth/login", {
    method: "POST",
    body: JSON.stringify({ email }),
  });
}

export async function registerUser(email: string): Promise<AuthResponse> {
  return fetchApi<AuthResponse>("/api/auth/register", {
    method: "POST",
    body: JSON.stringify({ email }),
  });
}
