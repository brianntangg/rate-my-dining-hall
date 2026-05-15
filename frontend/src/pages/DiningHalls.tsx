import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { schoolsApi } from '../api/schools';
import { Layout } from '../components/Layout';

export const DiningHalls: React.FC = () => {
  const navigate = useNavigate();

  const { data: diningHalls, isLoading, error } = useQuery({
    queryKey: ['diningHalls'],
    queryFn: () => schoolsApi.getDiningHalls(undefined),
  });

  if (isLoading) {
    return (
      <Layout>
        <div className="text-center py-12">
          <div className="text-lg text-gray-600">Loading dining halls...</div>
        </div>
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout>
        <div className="text-center py-12">
          <div className="text-lg text-red-600">Error loading dining halls</div>
        </div>
      </Layout>
    );
  }

  if (!diningHalls || diningHalls.length === 0) {
    return (
      <Layout>
        <div className="text-center py-12">
          <div className="text-lg text-gray-600">No dining halls found</div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="space-y-6">
        <h2 className="text-3xl font-bold text-gray-900">Vanderbilt Dining Halls</h2>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {diningHalls.map((hall) => (
            <div
              key={hall.id}
              onClick={() => navigate(`/halls/${hall.id}`)}
              className="bg-white rounded-lg shadow-md p-6 cursor-pointer hover:shadow-lg transition-shadow"
            >
              <h3 className="text-xl font-semibold text-gray-900 mb-2">{hall.name}</h3>
              {hall.average_rating !== null && hall.average_rating !== undefined ? (
                <div className="flex items-center">
                  <span className="text-2xl font-bold text-indigo-600">
                    {hall.average_rating.toFixed(1)}
                  </span>
                  <span className="text-gray-500 ml-2">/ 5.0</span>
                </div>
              ) : (
                <div className="text-gray-500">No reviews yet</div>
              )}
            </div>
          ))}
        </div>
      </div>
    </Layout>
  );
};
