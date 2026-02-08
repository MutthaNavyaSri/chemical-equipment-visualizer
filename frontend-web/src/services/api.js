import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_URL}/auth/token/refresh/`, {
            refresh: refreshToken,
          });
          const { access } = response.data;
          localStorage.setItem('access_token', access);
          originalRequest.headers.Authorization = `Bearer ${access}`;
          return api(originalRequest);
        } catch (err) {
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          window.location.href = '/login';
          return Promise.reject(err);
        }
      }
    }
    return Promise.reject(error);
  }
);

// Auth APIs
export const authAPI = {
  register: (userData) => api.post('/auth/register/', userData),
  login: (credentials) => api.post('/auth/login/', credentials),
  getProfile: () => api.get('/auth/profile/'),
};

// Dataset APIs
export const datasetAPI = {
  uploadCSV: (formData) => {
    return api.post('/datasets/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  getDatasets: () => api.get('/datasets/'),
  getDatasetDetail: (id) => api.get(`/datasets/${id}/`),
  deleteDataset: (id) => api.delete(`/datasets/${id}/delete/`),
  downloadReport: (id) => {
    return api.get(`/datasets/${id}/report/`, {
      responseType: 'blob',
    });
  },
};

export default api;
