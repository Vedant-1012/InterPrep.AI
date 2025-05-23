import axios from 'axios';

// API base URL - configurable for different environments
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001/api';

// Create axios instance
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
apiClient.interceptors.request.use(
  (config) => {
    const token = sessionStorage.getItem('accessToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Add response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Log errors for debugging
    console.error('API Error:', error.response?.data || error.message);
    
    // Enhance error object with more details
    const enhancedError = error;
    enhancedError.details = error.response?.data?.details || 'An unexpected error occurred';
    enhancedError.userMessage = error.response?.data?.message || 'Operation failed';
    
    return Promise.reject(enhancedError);
  }
);

// Questions API
export const questionsApi = {
  // Get questions with filters
  getQuestions: async (filters = {}) => {
    const { topic, difficulty, company, query, limit = 10, offset = 0 } = filters;
    let url = `/questions?limit=${limit}&offset=${offset}`;
    
    if (topic) url += `&topic=${encodeURIComponent(topic)}`;
    if (difficulty) url += `&difficulty=${encodeURIComponent(difficulty)}`;
    if (company) url += `&company=${encodeURIComponent(company)}`;
    if (query) url += `&query=${encodeURIComponent(query)}`;
    
    const response = await apiClient.get(url);
    return response.data;
  },
  
  // Get question details
  getQuestion: async (questionId) => {
    const response = await apiClient.get(`/questions/${questionId}`);
    return response.data;
  },
  
  // Generate a new question
  generateQuestion: async (data) => {
    const response = await apiClient.post(`/questions/generate`, data);
    return response.data;
  },
  
  // Generate a similar question
  generateSimilarQuestion: async (questionId) => {
    const response = await apiClient.post(`/questions/${questionId}/similar`);
    return response.data;
  },
  
  // Add question to favorites
  addToFavorites: async (questionId) => {
    const response = await apiClient.post(`/questions/${questionId}/favorite`);
    return response.data;
  },
  
  // Remove question from favorites
  removeFromFavorites: async (questionId) => {
    const response = await apiClient.delete(`/questions/${questionId}/favorite`);
    return response.data;
  }
};

// Submissions API
export const submissionsApi = {
  // Submit a solution
  submitSolution: async (data) => {
    const response = await apiClient.post(`/submissions`, data);
    return response.data;
  },
  
  // Get user submissions
  getSubmissions: async (filters = {}) => {
    const { questionId, status, limit = 10, offset = 0 } = filters;
    let url = `/submissions?limit=${limit}&offset=${offset}`;
    
    if (questionId) url += `&question_id=${questionId}`;
    if (status) url += `&status=${encodeURIComponent(status)}`;
    
    const response = await apiClient.get(url);
    return response.data;
  },
  
  // Get submission details
  getSubmission: async (submissionId) => {
    const response = await apiClient.get(`/submissions/${submissionId}`);
    return response.data;
  }
};

// User API
export const userApi = {
  // Get current user profile
  getCurrentUser: async () => {
    const response = await apiClient.get(`/users/me`);
    return response.data;
  },
  
  // Update user profile
  updateProfile: async (data) => {
    const response = await apiClient.put(`/users/me`, data);
    return response.data;
  },
  
  // Get user statistics
  // getUserStats: async () => {
  //   const response = await apiClient.get(`/users/me/stats`);
  //   return response.data;
  // },
  // Get user statistics
getUserStats: async () => {
  try {
    console.log("Calling /users/me/stats endpoint");
    const response = await apiClient.get(`/users/me/stats`);
    console.log("Raw response:", response);
    return response.data;
  } catch (error) {
    console.error("Error in getUserStats:", error);
    console.error("Error response data:", error.response?.data);
    throw error;
  }
},

  
  // Get user favorites
  getUserFavorites: async () => {
    const response = await apiClient.get(`/users/me/favorites`);
    return response.data;
  },
  
  // Get user practice history
  getUserHistory: async () => {
    const response = await apiClient.get(`/users/me/history`);
    return response.data;
  }
};

// Learning API
export const learningApi = {
  // Get all learning categories
  getCategories: async () => {
    const response = await apiClient.get(`/learning/categories`);
    return response.data;
  },

  getLearningStats: async () => {
  try {
    const response = await apiClient.get('/learning/stats');
    return response.data;
  } catch (error) {
    console.error("Error fetching learning stats:", error);
    throw error;
  }
},

// Get recommended learning topics
getRecommendations: async (limit = 3) => {
  // Dummy recommendation logic — later connect to a real ML-based recommender
  const response = await apiClient.get(`/learning/recommendations?limit=${limit}`);
  return response.data;
},
  
  // Get learning topics
  getTopics: async (categoryId = null) => {
    let url = `/learning/topics`;
    if (categoryId) url += `?category_id=${categoryId}`;
    
    const response = await apiClient.get(url);
    return response.data;
  },
  
  // Get content for a topic
  getTopicContent: async (topicId) => {
    const response = await apiClient.get(`/learning/topics/${topicId}/content`);
    return response.data;
  },
  
  // Get specific content
  getContent: async (contentId) => {
    const response = await apiClient.get(`/learning/content/${contentId}`);
    return response.data;
  },
  
  // Update learning progress
  updateProgress: async (data) => {
    const response = await apiClient.post(`/learning/progress`, data);
    return response.data;
  }
};

// Enhanced Practice API
export const practiceApi = {
  // Get a personalized practice session
  getPracticeSession: async (filters = {}) => {
    const { topic, difficulty, company, limit = 5 } = filters;
    let url = `/practice/session?limit=${limit}`;
    
    if (topic) url += `&topic=${encodeURIComponent(topic)}`;
    if (difficulty) url += `&difficulty=${encodeURIComponent(difficulty)}`;
    if (company) url += `&company=${encodeURIComponent(company)}`;
    
    const response = await apiClient.get(url);
    return response.data;
  },
  
  // Get practice progress
  getPracticeProgress: async () => {
    const response = await apiClient.get(`/practice/progress`);
    return response.data;
  },
  
  // Record practice activity
  recordActivity: async (data) => {
    const response = await apiClient.post(`/practice/activity`, data);
    return response.data;
  },
  
  // Evaluate solution
  evaluateSolution: async (data) => {
    const response = await apiClient.post(`/practice/evaluate`, data);
    return response.data;
  }
};

// Auth API
export const authApi = {
  login: (credentials) => apiClient.post('/auth/login', credentials),
  register: (userData) => apiClient.post('/auth/register', userData),
  refreshToken: () => apiClient.post('/auth/refresh'),
  logout: () => apiClient.post('/auth/logout'),
  getCurrentUser: () => apiClient.get('/auth/me')
};

export default apiClient;
