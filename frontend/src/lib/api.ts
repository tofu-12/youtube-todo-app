import type {
  AuthResponse,
  RecurrenceOut,
  RecurrenceRequest,
  SettingsOut,
  SettingsUpdateRequest,
  TodayVideoOut,
  TodoHistoryCreateRequest,
  TodoHistoryOut,
  VideoCreateRequest,
  VideoOut,
  VideoUpdateRequest,
  WorkoutHistoryCreateRequest,
  WorkoutHistoryOut,
} from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

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
    const body = await res.text();
    throw new Error(`API error ${res.status}: ${body}`);
  }

  if (res.status === 204) {
    return undefined as T;
  }

  return res.json() as Promise<T>;
}

// Videos

export async function getVideos(): Promise<VideoOut[]> {
  return fetchApi<VideoOut[]>("/api/videos", { cache: "no-store" });
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
