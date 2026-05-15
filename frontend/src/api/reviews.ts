import apiClient from './client';
import type { Review, ReviewCreate, VoteCreate, VotesResponse } from '../types';

export const reviewsApi = {
  getReviews: async (diningHallId: number, limit = 20, offset = 0): Promise<Review[]> => {
    const response = await apiClient.get<Review[]>('/api/reviews', {
      params: { dining_hall_id: diningHallId, limit, offset },
    });
    return response.data;
  },

  getReview: async (id: number): Promise<Review> => {
    const response = await apiClient.get<Review>(`/api/reviews/${id}`);
    return response.data;
  },

  createReview: async (data: ReviewCreate): Promise<Review> => {
    const response = await apiClient.post<Review>('/api/reviews', data);
    return response.data;
  },

  deleteReview: async (id: number): Promise<void> => {
    await apiClient.delete(`/api/reviews/${id}`);
  },

  vote: async (data: VoteCreate): Promise<VotesResponse> => {
    const response = await apiClient.post<VotesResponse>('/api/votes', data);
    return response.data;
  },
};
