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

    delete: async (id: number) => {
        await api.delete(`/calendars/${id}`);
    },

    update: async (id: number, data: CalendarUpdate) => {
        const response = await api.put<Calendar>(`/calendars/${id}`, data);
        return response.data;
    },

    calculateWorkingDays: async (id: number, startDate: string, endDate: string) => {
        const response = await api.get<WorkingDaysResponse>(`/calendars/${id}/working-days`, {
            params: { start_date: startDate, end_date: endDate },
        });
        return response.data;
    },

    importPublicHolidays: async (id: number, country: string, year: number) => {
        const response = await api.post<CalendarImportResponse>(`/calendars/${id}/import-holidays`, {
            source: 'public',
            country,
            year,
        });
        return response.data;
    },

    importHolidayCsv: async (id: number, csvText: string) => {
        const response = await api.post<CalendarImportResponse>(`/calendars/${id}/import-holidays`, {
            source: 'csv',
            csv_text: csvText,
        });
        return response.data;
    },
};
