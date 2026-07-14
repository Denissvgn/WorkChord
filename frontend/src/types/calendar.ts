export interface Calendar {
    id: number;
    name: string;
    year: number;
    holidays: string[]; // ISO date strings
    weekend_days: number[]; // 0=Mon .. 6=Sun (matches backend Calendar.weekend_days)
    short_days: string[]; // Pre-holiday shortened days
}

export interface CalendarCreate {
    name: string;
    year: number;
    holidays: string[];
    weekend_days: number[];
    short_days: string[];
}

export interface CalendarUpdate {
    name?: string;
    year?: number;
    holidays?: string[];
    weekend_days?: number[];
    short_days?: string[];
}

export interface WorkingDaysResponse {
    total_days: number;
    working_days: number;
    holidays: string[];
    weekends: string[];
}

export interface CalendarImportError {
    row: number;
    message: string;
}

export interface CalendarImportResponse {
    calendar: Calendar;
    imported_count: number;
    skipped_count: number;
    errors: CalendarImportError[];
}
