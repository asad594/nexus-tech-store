import axios from 'axios';

const API = axios.create({
  baseURL: '/api',
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

export default API;
