import axios from 'axios';

const API = axios.create({
  baseURL: '/api',
  timeout: 10000,
});

// Interceptor to inject JWT Access token into requests
API.interceptors.request.use((config) => {
  const token = localStorage.getItem('nexus_access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

// Interceptor to handle global response errors
API.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Handle unauthorized session expiration
    }
    return Promise.reject(error);
  }
);

export default API;
