import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Box, CircularProgress } from '@mui/material';
import { useAuth } from './context/AuthContext';

// Layout
import MainLayout from './components/layout/MainLayout';

// Pages
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Practice from './pages/Practice';
import PracticeQuestion from './pages/PracticeQuestion';
import Learning from './pages/Learning';
import LearningTopic from './pages/LearningTopic';
import Profile from './pages/Profile';
import NotFound from './pages/NotFound';

const App = () => {
  const { isAuthenticated, loading } = useAuth();

  // Protected route component
  const ProtectedRoute = ({ children }) => {
    if (loading) {
      return (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
          <CircularProgress />
        </Box>
      );
    }
    
    if (!isAuthenticated) {
      return <Navigate to="/login" />;
    }
    
    return children;
  };

  return (
    <Routes>
      {/* Public routes */}
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      
      {/* Protected routes */}
      <Route path="/dashboard" element={
        <ProtectedRoute>
          <MainLayout>
            <Dashboard />
          </MainLayout>
        </ProtectedRoute>
      } />
      
      <Route path="/practice" element={
        <ProtectedRoute>
          <MainLayout>
            <Practice />
          </MainLayout>
        </ProtectedRoute>
      } />
      
      <Route path="/practice/:questionId" element={
        <ProtectedRoute>
          <MainLayout>
            <PracticeQuestion />
          </MainLayout>
        </ProtectedRoute>
      } />
      
      <Route path="/learning" element={
        <ProtectedRoute>
          <MainLayout>
            <Learning />
          </MainLayout>
        </ProtectedRoute>
      } />
      
      <Route path="/learning/:topicId" element={
        <ProtectedRoute>
          <MainLayout>
            <LearningTopic />
          </MainLayout>
        </ProtectedRoute>
      } />
      
      <Route path="/profile" element={
        <ProtectedRoute>
          <MainLayout>
            <Profile />
          </MainLayout>
        </ProtectedRoute>
      } />
      
      {/* 404 route */}
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
};

export default App;
