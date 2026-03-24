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

export enum ScheduledStatus {
  OVERDUE = "overdue",
  TODAY = "today",
  UPCOMING = "upcoming",
  UNSCHEDULED = "unscheduled",
}

export enum VideoSortField {
  NAME = "name",
  CREATED_AT = "created_at",
  UPDATED_AT = "updated_at",
  NEXT_SCHEDULED_DATE = "next_scheduled_date",
  LAST_PERFORMED_DATE = "last_performed_date",
}

export enum SortOrder {
  ASC = "asc",
  DESC = "desc",
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
  workout_history_expires_days: number;
}

export interface TimezoneOption {
  value: string;
  label: string;
}

export interface PaginatedVideoOut {
  items: VideoOut[];
  total: number;
  skip: number;
  limit: number;
}

export interface VideoListParams {
  name?: string;
  tag_names?: string[];
  scheduled_status?: ScheduledStatus;
  sort_field?: VideoSortField;
  sort_order?: SortOrder;
  skip?: number;
  limit?: number;
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
  next_scheduled_date?: string | null;
}

export interface WorkoutHistoryCreateRequest {
  video_id: string;
}

export interface SettingsUpdateRequest {
  day_change_time?: string;
  timezone?: string;
  workout_history_expires_days?: number;
}
