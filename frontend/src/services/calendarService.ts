import { revisionHeaders, type ObservedRevisions } from './planningInputService';
import api from './api';
import type { Calendar, CalendarCreate, CalendarImportResponse, CalendarUpdate, WorkingDaysResponse } from '../types/calendar';

export const calendarService = {
    getAll: async () => {
        const response = await api.get<Calendar[]>('/calendars');
        return response.data;
    },

    getById: async (id: number) => {
        const response = await api.get<Calendar>(`/calendars/${id}`);
        return response.data;
    },

    create: async (data: CalendarCreate) => {
        const response = await api.post<Calendar>('/calendars', data);
        return response.data;
    },

    delete: async (id: number, revisions: ObservedRevisions) => {
        await api.delete(`/calendars/${id}`, { headers: revisionHeaders(revisions) });
    },

    update: async (id: number, data: CalendarUpdate, revisions: ObservedRevisions) => {
        const response = await api.put<Calendar>(`/calendars/${id}`, data, { headers: revisionHeaders(revisions) });
        return response.data;
    },

    calculateWorkingDays: async (id: number, startDate: string, endDate: string) => {
        const response = await api.get<WorkingDaysResponse>(`/calendars/${id}/working-days`, {
            params: { start_date: startDate, end_date: endDate },
        });
        return response.data;
    },

    importPublicHolidays: async (id: number, country: string, year: number, revisions: ObservedRevisions) => {
        const response = await api.post<CalendarImportResponse>(`/calendars/${id}/import-holidays`, {
            source: 'public',
            country,
            year,
        }, { headers: revisionHeaders(revisions) });
        return response.data;
    },

    importHolidayCsv: async (id: number, csvText: string, revisions: ObservedRevisions) => {
        const response = await api.post<CalendarImportResponse>(`/calendars/${id}/import-holidays`, {
            source: 'csv',
            csv_text: csvText,
        }, { headers: revisionHeaders(revisions) });
        return response.data;
    },
};
