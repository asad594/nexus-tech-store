import React, { createContext, useContext, useState, useEffect } from 'react';
import API from '../api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('nexus_access_token') || null);
  const [loading, setLoading] = useState(true);

  const fetchProfile = async () => {
    try {
      const response = await API.get('/auth/me/');
      setUser(response.data);
    } catch (err) {
      console.error('Failed to fetch user profile', err);
      logout();
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (token) {
      fetchProfile();
    } else {
      setUser(null);
      setLoading(false);
    }
  }, [token]);

  const login = async (username, password) => {
    const response = await API.post('/auth/token/', { username, password });
    const { access, refresh } = response.data;
    localStorage.setItem('nexus_access_token', access);
    localStorage.setItem('nexus_refresh_token', refresh);
    setToken(access);
    const profileRes = await API.get('/auth/me/', {
      headers: { Authorization: `Bearer ${access}` }
    });
    setUser(profileRes.data);
    return profileRes.data;
  };

  const register = async (userData) => {
    try {
      await API.post('/auth/register/', userData);
      return await login(userData.username, userData.password);
    } catch (err) {
      if (err.response && err.response.data) {
        throw err.response.data;
      }
      throw err;
    }
  };

  const logout = () => {
    localStorage.removeItem('nexus_access_token');
    localStorage.removeItem('nexus_refresh_token');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, login, register, logout, fetchProfile }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
