import apiClient from './client';
import type { School, DiningHall } from '../types';

export const schoolsApi = {
  getSchools: async (): Promise<School[]> => {
    const response = await apiClient.get<School[]>('/api/schools');
    return response.data;
  },

  getDiningHalls: async (schoolId?: number): Promise<DiningHall[]> => {
    const params = schoolId ? { school_id: schoolId } : undefined;
    const response = await apiClient.get<DiningHall[]>('/api/dining-halls', { params });
    return response.data;
  },

  getDiningHall: async (id: number): Promise<DiningHall> => {
    const response = await apiClient.get<DiningHall>(`/api/dining-halls/${id}`);
    return response.data;
  },
};
