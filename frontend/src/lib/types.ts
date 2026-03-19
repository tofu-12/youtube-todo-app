// Enums

export enum RecurrenceType {
  NONE = "none",
  DAILY = "daily",
  WEEKLY = "weekly",
  INTERVAL = "interval",
}

export enum DayOfWeek {
  MON = "mon",
  TUE = "tue",
  WED = "wed",
  THU = "thu",
  FRI = "fri",
  SAT = "sat",
  SUN = "sun",
}

export enum TodoStatus {
  COMPLETED = "completed",
  SKIPPED = "skipped",
}

// Auth types

export interface AuthResponse {
  id: string;
  email: string;
}

// Response types

export interface TagOut {
  id: string;
  name: string;
}

export interface VideoOut {
  id: string;
  name: string;
  url: string;
  comment: string | null;
  last_performed_date: string | null;
  next_scheduled_date: string | null;
  tags: TagOut[];
  created_at: string;
  updated_at: string;
}

export interface TodayVideoOut {
  id: string;
  name: string;
  url: string;
  comment: string | null;
  next_scheduled_date: string | null;
  tags: TagOut[];
}

export interface RecurrenceOut {
  id: string;
  recurrence_type: RecurrenceType;
  interval_days: number | null;
  weekdays: DayOfWeek[];
  created_at: string;
  updated_at: string;
}

export interface TodoHistoryOut {
  id: string;
  video_id: string;
  scheduled_date: string;
  status: TodoStatus;
  created_at: string;
  updated_at: string;
}

export interface WorkoutHistoryOut {
  id: string;
  video_id: string;
  performed_date: string;
  performed_at: string;
  expires_date: string;
  created_at: string;
  updated_at: string;
}

export interface SettingsOut {
  day_change_time: string;
  timezone: string;
}

export interface TimezoneOption {
  value: string;
  label: string;
}

// Request types

export interface VideoCreateRequest {
  name: string;
  url: string;
  comment?: string | null;
  next_scheduled_date?: string | null;
  tag_names?: string[];
}

export interface VideoUpdateRequest {
  name?: string;
  url?: string;
  comment?: string | null;
  next_scheduled_date?: string | null;
  tag_names?: string[];
}

export interface RecurrenceRequest {
  recurrence_type: RecurrenceType;
  interval_days?: number | null;
  weekdays?: DayOfWeek[];
}

export interface TodoHistoryCreateRequest {
  video_id: string;
  scheduled_date: string;
  status: TodoStatus;
}

export interface WorkoutHistoryCreateRequest {
  video_id: string;
  expires_days: number;
}

export interface SettingsUpdateRequest {
  day_change_time?: string;
  timezone?: string;
}
