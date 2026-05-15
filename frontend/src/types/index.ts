export interface User {
  id: number;
  email: string;
  school_id: number;
}

export interface School {
  id: number;
  name: string;
  allowed_domain: string;
}

export interface DiningHall {
  id: number;
  name: string;
  school_id: number;
  average_rating?: number;
}

export interface Review {
  id: number;
  user_id: number;
  dining_hall_id: number;
  rating: number;
  text: string;
  created_at: string;
  upvotes: number;
  downvotes: number;
  score: number;
}

export interface ReviewCreate {
  dining_hall_id: number;
  rating: number;
  text: string;
}

export interface VoteCreate {
  review_id: number;
  value: 1 | -1;
}

export interface VotesResponse {
  upvotes: number;
  downvotes: number;
  score: number;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}
