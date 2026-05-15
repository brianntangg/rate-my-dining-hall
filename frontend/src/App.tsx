import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { AuthProvider } from './contexts/AuthContext';
import { ProtectedRoute } from './components/ProtectedRoute';
import { Register } from './pages/Register';
import { Login } from './pages/Login';
import { DiningHalls } from './pages/DiningHalls';
import { DiningHallDetail } from './pages/DiningHallDetail';
import { ReviewForm } from './pages/ReviewForm';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AuthProvider>
          <Routes>
            <Route path="/" element={<Navigate to="/halls" replace />} />
            <Route path="/register" element={<Register />} />
            <Route path="/login" element={<Login />} />
            <Route
              path="/halls"
              element={
                <ProtectedRoute>
                  <DiningHalls />
                </ProtectedRoute>
              }
            />
            <Route
              path="/halls/:id"
              element={
                <ProtectedRoute>
                  <DiningHallDetail />
                </ProtectedRoute>
              }
            />
            <Route
              path="/halls/:id/review"
              element={
                <ProtectedRoute>
                  <ReviewForm />
                </ProtectedRoute>
              }
            />
          </Routes>
          <ToastContainer
            position="top-right"
            autoClose={3000}
            hideProgressBar={false}
            newestOnTop
            closeOnClick
            rtl={false}
            pauseOnFocusLoss
            draggable
            pauseOnHover
          />
        </AuthProvider>
      </BrowserRouter>
    </QueryClientProvider>
  );
};

export default App;
