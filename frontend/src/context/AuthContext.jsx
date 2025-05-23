import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

// Create context
const AuthContext = createContext();

// Custom hook to use the auth context
export const useAuth = () => useContext(AuthContext);

// Utility functions for token management (more secure than localStorage)
const tokenStorage = {
  getAccessToken: () => sessionStorage.getItem('accessToken'),
  getRefreshToken: () => sessionStorage.getItem('refreshToken'),
  setAccessToken: (token) => sessionStorage.setItem('accessToken', token),
  setRefreshToken: (token) => sessionStorage.setItem('refreshToken', token),
  clearTokens: () => {
    sessionStorage.removeItem('accessToken');
    sessionStorage.removeItem('refreshToken');
  }
};

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Initialize auth state from storage
  useEffect(() => {
    const initializeAuth = async () => {
      try {
        const accessToken = tokenStorage.getAccessToken();
        const refreshToken = tokenStorage.getRefreshToken();
        
        if (!accessToken || !refreshToken) {
          setLoading(false);
          return;
        }
        
        // Check if token is expired
        const decodedToken = jwtDecode(accessToken);
        const currentTime = Date.now() / 1000;
        
        if (decodedToken.exp < currentTime) {
          // Token expired, try to refresh
          await refreshAccessToken();
        } else {
          // Token valid, set auth state
          setAuthState(accessToken);
        }
      } catch (error) {
        console.error('Auth initialization error:', error);
        logout();
      } finally {
        setLoading(false);
      }
    };
    
    initializeAuth();
  }, []);

  // Set authentication state based on token
  const setAuthState = (token) => {
    if (token) {
      const decodedToken = jwtDecode(token);
      setCurrentUser({ id: decodedToken.sub });
      setIsAuthenticated(true);
      
      // Set authorization header for all future requests
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    }
  };

  // Register a new user with enhanced error handling
  const register = async (username, email, password) => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await axios.post('/api/auth/register', {
        username,
        email,
        password
      });
      
      const { access_token, refresh_token } = response.data;
      
      // Store tokens securely
      tokenStorage.setAccessToken(access_token);
      tokenStorage.setRefreshToken(refresh_token);
      
      // Set auth state
      setAuthState(access_token);
      
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Registration failed';
      const errorDetails = error.response?.data?.details || 'Please check your information and try again';
      
      setError({ message: errorMessage, details: errorDetails });
      throw error;
    } finally {
      setLoading(false);
    }
  };

  // Login user with enhanced error handling
  const login = async (username, password) => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await axios.post('/api/auth/login', {
        username,
        password
      });
      
      const { access_token, refresh_token } = response.data;
      
      // Store tokens securely
      tokenStorage.setAccessToken(access_token);
      tokenStorage.setRefreshToken(refresh_token);
      
      // Set auth state
      setAuthState(access_token);
      
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Login failed';
      const errorDetails = error.response?.data?.details || 'Please check your credentials and try again';
      
      setError({ message: errorMessage, details: errorDetails });
      throw error;
    } finally {
      setLoading(false);
    }
  };

  // Refresh access token with enhanced error handling
  const refreshAccessToken = async () => {
    try {
      const refreshToken = tokenStorage.getRefreshToken();
      
      if (!refreshToken) {
        throw new Error('No refresh token available');
      }
      
      // Set refresh token in header for this request
      const response = await axios.post('/api/auth/refresh', {}, {
        headers: {
          'Authorization': `Bearer ${refreshToken}`
        }
      });
      
      const { access_token } = response.data;
      
      // Store new access token
      tokenStorage.setAccessToken(access_token);
      
      // Set auth state
      setAuthState(access_token);
      
      return access_token;
    } catch (error) {
      console.error('Token refresh failed:', error);
      logout();
      throw error;
    }
  };

  // Logout user
  const logout = () => {
    // Remove tokens from storage
    tokenStorage.clearTokens();
    
    // Clear auth state
    setCurrentUser(null);
    setIsAuthenticated(false);
    
    // Remove authorization header
    delete axios.defaults.headers.common['Authorization'];
  };

  // Create axios response interceptor to handle token expiration
  useEffect(() => {
    const interceptor = axios.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config;
        
        // If error is 401 and not a retry
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;
          
          try {
            // Refresh token
            const newToken = await refreshAccessToken();
            
            // Retry original request with new token
            originalRequest.headers['Authorization'] = `Bearer ${newToken}`;
            return axios(originalRequest);
          } catch (refreshError) {
            return Promise.reject(refreshError);
          }
        }
        
        return Promise.reject(error);
      }
    );
    
    // Clean up interceptor on unmount
    return () => {
      axios.interceptors.response.eject(interceptor);
    };
  }, []);

  // Context value
  const value = {
    currentUser,
    isAuthenticated,
    loading,
    error,
    register,
    login,
    logout,
    refreshAccessToken
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
