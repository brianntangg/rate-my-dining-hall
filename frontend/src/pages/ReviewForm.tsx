import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useMutation, useQueryClient, useQuery } from '@tanstack/react-query';
import { reviewsApi } from '../api/reviews';
import { schoolsApi } from '../api/schools';
import { Layout } from '../components/Layout';
import { toast } from 'react-toastify';

export const ReviewForm: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const diningHallId = parseInt(id || '0', 10);

  const [rating, setRating] = useState<number>(5);
  const [text, setText] = useState('');
  const [hoveredRating, setHoveredRating] = useState<number | null>(null);

  const { data: diningHall } = useQuery({
    queryKey: ['diningHall', diningHallId],
    queryFn: () => schoolsApi.getDiningHall(diningHallId),
    enabled: !!diningHallId,
  });

  const createReviewMutation = useMutation({
    mutationFn: () =>
      reviewsApi.createReview({
        dining_hall_id: diningHallId,
        rating,
        text,
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['reviews', diningHallId] });
      queryClient.invalidateQueries({ queryKey: ['diningHall', diningHallId] });
      queryClient.invalidateQueries({ queryKey: ['diningHalls'] });
      toast.success('Review submitted successfully!');
      navigate(`/halls/${diningHallId}`);
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (text.trim().length < 10) {
      toast.error('Review text must be at least 10 characters');
      return;
    }

    createReviewMutation.mutate();
  };

  return (
    <Layout>
      <div className="max-w-2xl mx-auto">
        <div className="bg-white rounded-lg shadow-md p-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            Write a Review
            {diningHall && (
              <span className="block text-xl text-gray-600 mt-2">{diningHall.name}</span>
            )}
          </h2>

          <form onSubmit={handleSubmit} className="mt-6 space-y-6">
            {/* Rating */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Rating <span className="text-red-500">*</span>
              </label>
              <div className="flex items-center gap-2">
                {[1, 2, 3, 4, 5].map((star) => (
                  <button
                    key={star}
                    type="button"
                    onClick={() => setRating(star)}
                    onMouseEnter={() => setHoveredRating(star)}
                    onMouseLeave={() => setHoveredRating(null)}
                    className="text-4xl focus:outline-none"
                  >
                    <span
                      className={
                        star <= (hoveredRating || rating)
                          ? 'text-yellow-400'
                          : 'text-gray-300'
                      }
                    >
                      ★
                    </span>
                  </button>
                ))}
                <span className="ml-2 text-gray-600">{rating}/5</span>
              </div>
            </div>

            {/* Review text */}
            <div>
              <label htmlFor="text" className="block text-sm font-medium text-gray-700 mb-2">
                Review <span className="text-red-500">*</span>
              </label>
              <textarea
                id="text"
                rows={6}
                value={text}
                onChange={(e) => setText(e.target.value)}
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                placeholder="Share your experience... (minimum 10 characters)"
                required
              />
              <p className="mt-1 text-sm text-gray-500">{text.length} characters</p>
            </div>

            {/* Buttons */}
            <div className="flex gap-4">
              <button
                type="submit"
                disabled={createReviewMutation.isPending}
                className="flex-1 px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-gray-400 disabled:cursor-not-allowed"
              >
                {createReviewMutation.isPending ? 'Submitting...' : 'Submit Review'}
              </button>
              <button
                type="button"
                onClick={() => navigate(`/halls/${diningHallId}`)}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </Layout>
  );
};
