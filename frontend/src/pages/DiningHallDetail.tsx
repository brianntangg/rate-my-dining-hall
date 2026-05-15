import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useParams, useNavigate } from 'react-router-dom';
import { schoolsApi } from '../api/schools';
import { reviewsApi } from '../api/reviews';
import { Layout } from '../components/Layout';
import { useAuth } from '../contexts/AuthContext';
import { toast } from 'react-toastify';
import type { Review } from '../types';

export const DiningHallDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const { user } = useAuth();
  const [votingReviewId, setVotingReviewId] = useState<number | null>(null);

  const diningHallId = parseInt(id || '0', 10);

  const { data: diningHall, isLoading: hallLoading } = useQuery({
    queryKey: ['diningHall', diningHallId],
    queryFn: () => schoolsApi.getDiningHall(diningHallId),
    enabled: !!diningHallId,
  });

  const { data: reviews, isLoading: reviewsLoading } = useQuery({
    queryKey: ['reviews', diningHallId],
    queryFn: () => reviewsApi.getReviews(diningHallId),
    enabled: !!diningHallId,
  });

  const voteMutation = useMutation({
    mutationFn: (data: { reviewId: number; value: 1 | -1 }) =>
      reviewsApi.vote({ review_id: data.reviewId, value: data.value }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['reviews', diningHallId] });
      setVotingReviewId(null);
    },
    onError: () => {
      setVotingReviewId(null);
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (reviewId: number) => reviewsApi.deleteReview(reviewId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['reviews', diningHallId] });
      queryClient.invalidateQueries({ queryKey: ['diningHall', diningHallId] });
      toast.success('Review deleted successfully');
    },
  });

  const handleVote = (reviewId: number, value: 1 | -1) => {
    setVotingReviewId(reviewId);
    voteMutation.mutate({ reviewId, value });
  };

  const handleDelete = (reviewId: number) => {
    if (window.confirm('Are you sure you want to delete this review?')) {
      deleteMutation.mutate(reviewId);
    }
  };

  if (hallLoading || reviewsLoading) {
    return (
      <Layout>
        <div className="text-center py-12">
          <div className="text-lg text-gray-600">Loading...</div>
        </div>
      </Layout>
    );
  }

  if (!diningHall) {
    return (
      <Layout>
        <div className="text-center py-12">
          <div className="text-lg text-red-600">Dining hall not found</div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="space-y-8">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex justify-between items-start">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-2">{diningHall.name}</h2>
              {diningHall.average_rating !== null && diningHall.average_rating !== undefined ? (
                <div className="flex items-center">
                  <span className="text-3xl font-bold text-indigo-600">
                    {diningHall.average_rating.toFixed(1)}
                  </span>
                  <span className="text-gray-500 ml-2">/ 5.0</span>
                </div>
              ) : (
                <div className="text-gray-500">No reviews yet</div>
              )}
            </div>
            <button
              onClick={() => navigate(`/halls/${diningHallId}/review`)}
              className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Write a Review
            </button>
          </div>
        </div>

        {/* Reviews */}
        <div className="space-y-4">
          <h3 className="text-2xl font-bold text-gray-900">Reviews</h3>

          {!reviews || reviews.length === 0 ? (
            <div className="bg-white rounded-lg shadow-md p-6 text-center text-gray-500">
              No reviews yet. Be the first to review!
            </div>
          ) : (
            <div className="space-y-4">
              {reviews.map((review: Review) => (
                <div key={review.id} className="bg-white rounded-lg shadow-md p-6">
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <div className="flex items-center mb-2">
                        {[...Array(5)].map((_, i) => (
                          <span
                            key={i}
                            className={`text-xl ${
                              i < review.rating ? 'text-yellow-400' : 'text-gray-300'
                            }`}
                          >
                            ★
                          </span>
                        ))}
                      </div>
                      <p className="text-gray-700">{review.text}</p>
                      <p className="text-sm text-gray-500 mt-2">
                        {new Date(review.created_at).toLocaleDateString()}
                      </p>
                    </div>
                    {user?.id === review.user_id && (
                      <button
                        onClick={() => handleDelete(review.id)}
                        className="px-3 py-1 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700"
                        disabled={deleteMutation.isPending}
                      >
                        Delete
                      </button>
                    )}
                  </div>

                  {/* Vote buttons */}
                  {user?.id !== review.user_id && (
                    <div className="flex items-center gap-4 pt-4 border-t">
                      <button
                        onClick={() => handleVote(review.id, 1)}
                        disabled={votingReviewId === review.id}
                        className="flex items-center gap-2 px-3 py-1 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 disabled:opacity-50"
                      >
                        ▲ {review.upvotes}
                      </button>
                      <button
                        onClick={() => handleVote(review.id, -1)}
                        disabled={votingReviewId === review.id}
                        className="flex items-center gap-2 px-3 py-1 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 disabled:opacity-50"
                      >
                        ▼ {review.downvotes}
                      </button>
                      <span className="text-sm font-medium text-gray-700">
                        Score: {review.score}
                      </span>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
};
