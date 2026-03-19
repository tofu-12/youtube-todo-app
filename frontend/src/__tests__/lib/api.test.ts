import {
  getVideos,
  getVideo,
  createVideo,
  updateVideo,
  deleteVideo,
  getRecurrence,
  upsertRecurrence,
  getTodayVideos,
  getOverdueVideos,
  getTodoHistories,
  createTodoHistory,
  getWorkoutHistories,
  createWorkoutHistory,
  getTimezones,
  getSettings,
  updateSettings,
} from "@/lib/api";
import { RecurrenceType, TodoStatus } from "@/lib/types";

const API_URL = "http://localhost:8000";

function mockFetchResponse(body: unknown, status = 200) {
  const response = {
    ok: status >= 200 && status < 300,
    status,
    json: () => Promise.resolve(body),
    text: () => Promise.resolve(JSON.stringify(body)),
  } as Response;
  return vi.fn().mockResolvedValue(response);
}

function mockFetch204() {
  const response = {
    ok: true,
    status: 204,
    json: () => Promise.resolve(undefined),
    text: () => Promise.resolve(""),
  } as Response;
  return vi.fn().mockResolvedValue(response);
}

function mockFetchError(status: number, body: string) {
  const response = {
    ok: false,
    status,
    text: () => Promise.resolve(body),
  } as Response;
  return vi.fn().mockResolvedValue(response);
}

beforeEach(() => {
  vi.stubGlobal("fetch", vi.fn());
});

afterEach(() => {
  vi.restoreAllMocks();
});

describe("fetchApi common behavior", () => {
  it("parses JSON response", async () => {
    vi.stubGlobal("fetch", mockFetchResponse([{ id: "1" }]));
    const result = await getVideos();
    expect(result).toEqual([{ id: "1" }]);
  });

  it("returns undefined for 204", async () => {
    vi.stubGlobal("fetch", mockFetch204());
    const result = await deleteVideo("1");
    expect(result).toBeUndefined();
  });

  it("throws on error status", async () => {
    vi.stubGlobal("fetch", mockFetchError(500, "Internal Server Error"));
    await expect(getVideos()).rejects.toThrow("API error 500: Internal Server Error");
  });
});

describe("getVideos", () => {
  it("calls GET /api/videos with cache no-store", async () => {
    const fetchMock = mockFetchResponse([]);
    vi.stubGlobal("fetch", fetchMock);
    await getVideos();
    expect(fetchMock).toHaveBeenCalledWith(`${API_URL}/api/videos`, {
      cache: "no-store",
      headers: { "Content-Type": "application/json" },
    });
  });
});

describe("getVideo", () => {
  it("calls GET /api/videos/{id}", async () => {
    const fetchMock = mockFetchResponse({ id: "abc" });
    vi.stubGlobal("fetch", fetchMock);
    const result = await getVideo("abc");
    expect(result).toEqual({ id: "abc" });
    expect(fetchMock).toHaveBeenCalledWith(`${API_URL}/api/videos/abc`, {
      cache: "no-store",
      headers: { "Content-Type": "application/json" },
    });
  });
});

describe("createVideo", () => {
  it("calls POST with JSON body", async () => {
    const data = { name: "Test", url: "https://youtube.com/watch?v=1" };
    const fetchMock = mockFetchResponse({ id: "new-id", ...data });
    vi.stubGlobal("fetch", fetchMock);
    await createVideo(data);
    expect(fetchMock).toHaveBeenCalledWith(`${API_URL}/api/videos`, {
      method: "POST",
      body: JSON.stringify(data),
      headers: { "Content-Type": "application/json" },
    });
  });
});

describe("updateVideo", () => {
  it("calls PUT /api/videos/{id}", async () => {
    const data = { name: "Updated" };
    const fetchMock = mockFetchResponse({ id: "1", ...data });
    vi.stubGlobal("fetch", fetchMock);
    await updateVideo("1", data);
    expect(fetchMock).toHaveBeenCalledWith(`${API_URL}/api/videos/1`, {
      method: "PUT",
      body: JSON.stringify(data),
      headers: { "Content-Type": "application/json" },
    });
  });
});

describe("deleteVideo", () => {
  it("calls DELETE /api/videos/{id}", async () => {
    const fetchMock = mockFetch204();
    vi.stubGlobal("fetch", fetchMock);
    await deleteVideo("1");
    expect(fetchMock).toHaveBeenCalledWith(`${API_URL}/api/videos/1`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
    });
  });
});

describe("getRecurrence", () => {
  it("returns RecurrenceOut on success", async () => {
    const rec = { id: "r1", recurrence_type: "daily" };
    vi.stubGlobal("fetch", mockFetchResponse(rec));
    const result = await getRecurrence("v1");
    expect(result).toEqual(rec);
  });

  it("returns null on 404", async () => {
    vi.stubGlobal("fetch", mockFetchError(404, "Not Found"));
    const result = await getRecurrence("v1");
    expect(result).toBeNull();
  });

  it("rethrows non-404 errors", async () => {
    vi.stubGlobal("fetch", mockFetchError(500, "Server Error"));
    await expect(getRecurrence("v1")).rejects.toThrow("API error 500");
  });
});

describe("upsertRecurrence", () => {
  it("calls PUT /api/videos/{id}/recurrence", async () => {
    const data = { recurrence_type: RecurrenceType.DAILY };
    const fetchMock = mockFetchResponse({ id: "r1", ...data });
    vi.stubGlobal("fetch", fetchMock);
    await upsertRecurrence("v1", data);
    expect(fetchMock).toHaveBeenCalledWith(
      `${API_URL}/api/videos/v1/recurrence`,
      {
        method: "PUT",
        body: JSON.stringify(data),
        headers: { "Content-Type": "application/json" },
      }
    );
  });
});

describe("getTodayVideos", () => {
  it("calls GET /api/today", async () => {
    const fetchMock = mockFetchResponse([]);
    vi.stubGlobal("fetch", fetchMock);
    await getTodayVideos();
    expect(fetchMock).toHaveBeenCalledWith(`${API_URL}/api/today`, {
      cache: "no-store",
      headers: { "Content-Type": "application/json" },
    });
  });
});

describe("getOverdueVideos", () => {
  it("calls GET /api/overdue", async () => {
    const fetchMock = mockFetchResponse([]);
    vi.stubGlobal("fetch", fetchMock);
    await getOverdueVideos();
    expect(fetchMock).toHaveBeenCalledWith(`${API_URL}/api/overdue`, {
      cache: "no-store",
      headers: { "Content-Type": "application/json" },
    });
  });
});

describe("getTodoHistories", () => {
  it("calls without query params when no scheduledDate", async () => {
    const fetchMock = mockFetchResponse([]);
    vi.stubGlobal("fetch", fetchMock);
    await getTodoHistories();
    expect(fetchMock).toHaveBeenCalledWith(`${API_URL}/api/todo-histories`, {
      cache: "no-store",
      headers: { "Content-Type": "application/json" },
    });
  });

  it("includes scheduled_date query param", async () => {
    const fetchMock = mockFetchResponse([]);
    vi.stubGlobal("fetch", fetchMock);
    await getTodoHistories("2026-01-01");
    expect(fetchMock).toHaveBeenCalledWith(
      `${API_URL}/api/todo-histories?scheduled_date=2026-01-01`,
      {
        cache: "no-store",
        headers: { "Content-Type": "application/json" },
      }
    );
  });
});

describe("createTodoHistory", () => {
  it("calls POST /api/todo-histories", async () => {
    const data = {
      video_id: "v1",
      scheduled_date: "2026-01-01",
      status: TodoStatus.COMPLETED,
    };
    const fetchMock = mockFetchResponse({ id: "th1", ...data });
    vi.stubGlobal("fetch", fetchMock);
    await createTodoHistory(data);
    expect(fetchMock).toHaveBeenCalledWith(`${API_URL}/api/todo-histories`, {
      method: "POST",
      body: JSON.stringify(data),
      headers: { "Content-Type": "application/json" },
    });
  });
});

describe("getWorkoutHistories", () => {
  it("calls without query params when no expiresAfter", async () => {
    const fetchMock = mockFetchResponse([]);
    vi.stubGlobal("fetch", fetchMock);
    await getWorkoutHistories();
    expect(fetchMock).toHaveBeenCalledWith(
      `${API_URL}/api/workout-histories`,
      {
        cache: "no-store",
        headers: { "Content-Type": "application/json" },
      }
    );
  });

  it("includes expires_after query param", async () => {
    const fetchMock = mockFetchResponse([]);
    vi.stubGlobal("fetch", fetchMock);
    await getWorkoutHistories("2026-01-01");
    expect(fetchMock).toHaveBeenCalledWith(
      `${API_URL}/api/workout-histories?expires_after=2026-01-01`,
      {
        cache: "no-store",
        headers: { "Content-Type": "application/json" },
      }
    );
  });
});

describe("createWorkoutHistory", () => {
  it("calls POST /api/workout-histories", async () => {
    const data = { video_id: "v1", expires_days: 7 };
    const fetchMock = mockFetchResponse({ id: "wh1", ...data });
    vi.stubGlobal("fetch", fetchMock);
    await createWorkoutHistory(data);
    expect(fetchMock).toHaveBeenCalledWith(
      `${API_URL}/api/workout-histories`,
      {
        method: "POST",
        body: JSON.stringify(data),
        headers: { "Content-Type": "application/json" },
      }
    );
  });
});

describe("getTimezones", () => {
  it("calls GET /api/settings/timezones", async () => {
    const data = [{ value: "Asia/Tokyo", label: "Asia/Tokyo" }];
    const fetchMock = mockFetchResponse(data);
    vi.stubGlobal("fetch", fetchMock);
    const result = await getTimezones();
    expect(result).toEqual(data);
    expect(fetchMock).toHaveBeenCalledWith(
      `${API_URL}/api/settings/timezones`,
      {
        cache: "no-store",
        headers: { "Content-Type": "application/json" },
      }
    );
  });
});

describe("getSettings", () => {
  it("calls GET /api/settings", async () => {
    const fetchMock = mockFetchResponse({ day_change_time: "04:00", timezone: "Asia/Tokyo" });
    vi.stubGlobal("fetch", fetchMock);
    const result = await getSettings();
    expect(result).toEqual({ day_change_time: "04:00", timezone: "Asia/Tokyo" });
  });
});

describe("updateSettings", () => {
  it("calls PUT /api/settings", async () => {
    const data = { day_change_time: "05:00" };
    const fetchMock = mockFetchResponse({ day_change_time: "05:00", timezone: "Asia/Tokyo" });
    vi.stubGlobal("fetch", fetchMock);
    await updateSettings(data);
    expect(fetchMock).toHaveBeenCalledWith(`${API_URL}/api/settings`, {
      method: "PUT",
      body: JSON.stringify(data),
      headers: { "Content-Type": "application/json" },
    });
  });
});
