import React, { useState } from 'react';
import { X, User, Lock, Mail, Shield, Sparkles, KeyRound } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const AuthModal = ({ isOpen, onClose }) => {
  const { login, register } = useAuth();
  const [isLoginTab, setIsLoginTab] = useState(true);

  // Form State
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [role, setRole] = useState('customer');

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      if (isLoginTab) {
        await login(username, password);
      } else {
        await register({ username, email, password, name, role });
      }
      onClose();
    } catch (err) {
      console.error('Auth error', err);
      if (err?.code === 'ERR_NETWORK' || !err?.response || err?.response?.status >= 500) {
        setError('Unable to connect to backend server. Please ensure the Django backend server is running at http://localhost:8000.');
      } else if (err?.response?.status === 401) {
        setError('Invalid username or password. Please try again.');
      } else {
        setError(err.response?.data?.error || err.response?.data?.detail || 'Authentication failed. Please verify credentials.');
      }
    } finally {
      setLoading(false);
    }
  };

  const fillDemoAdmin = () => {
    setIsLoginTab(true);
    setUsername('admin');
    setPassword('admin123');
  };

  const fillDemoCustomer = () => {
    setIsLoginTab(true);
    setUsername('john_doe');
    setPassword('password123');
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-fade-in">
      <div className="relative w-full max-w-md glass-panel rounded-3xl p-6 md:p-8 shadow-2xl border border-white/10 text-slate-100">
        
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-5 right-5 p-2 rounded-full glass-pill text-slate-400 hover:text-white cursor-pointer"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Header Tabs */}
        <div className="flex items-center justify-center space-x-2 bg-white/[0.04] p-1 rounded-full border border-white/10 mb-6">
          <button
            onClick={() => { setIsLoginTab(true); setError(null); }}
            className={`flex-1 py-2 rounded-full text-xs font-bold transition-all cursor-pointer ${
              isLoginTab ? 'bg-gradient-blue text-white shadow-md' : 'text-slate-400 hover:text-white'
            }`}
          >
            Sign In
          </button>
          <button
            onClick={() => { setIsLoginTab(false); setError(null); }}
            className={`flex-1 py-2 rounded-full text-xs font-bold transition-all cursor-pointer ${
              !isLoginTab ? 'bg-gradient-blue text-white shadow-md' : 'text-slate-400 hover:text-white'
            }`}
          >
            Register
          </button>
        </div>

        <h3 className="text-xl font-extrabold text-white text-center mb-1">
          {isLoginTab ? 'Welcome Back to NEXUS' : 'Create Quantum Account'}
        </h3>
        <p className="text-xs text-slate-400 text-center mb-6">
          {isLoginTab ? 'Access your cart, order history, and custom specs' : 'Join the next generation of tech enthusiasts'}
        </p>

        {error && (
          <div className="p-3 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-xs mb-4 text-center">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          {!isLoginTab && (
            <>
              <div className="space-y-1">
                <label className="text-xs font-bold text-slate-300">Full Name</label>
                <div className="relative">
                  <User className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Alex Nexus"
                    required
                    className="w-full pl-9 pr-4 py-2.5 rounded-xl bg-white/[0.04] border border-white/10 text-white text-xs focus:border-blue-400 focus:outline-none"
                  />
                </div>
              </div>

              <div className="space-y-1">
                <label className="text-xs font-bold text-slate-300">Email Address</label>
                <div className="relative">
                  <Mail className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="alex@nexus.io"
                    required
                    className="w-full pl-9 pr-4 py-2.5 rounded-xl bg-white/[0.04] border border-white/10 text-white text-xs focus:border-blue-400 focus:outline-none"
                  />
                </div>
              </div>
            </>
          )}

          <div className="space-y-1">
            <label className="text-xs font-bold text-slate-300">Username</label>
            <div className="relative">
              <User className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="john_doe"
                required
                className="w-full pl-9 pr-4 py-2.5 rounded-xl bg-white/[0.04] border border-white/10 text-white text-xs focus:border-blue-400 focus:outline-none"
              />
            </div>
          </div>

          <div className="space-y-1">
            <label className="text-xs font-bold text-slate-300">Password</label>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
                className="w-full pl-9 pr-4 py-2.5 rounded-xl bg-white/[0.04] border border-white/10 text-white text-xs focus:border-blue-400 focus:outline-none"
              />
            </div>
          </div>

          {!isLoginTab && (
            <div className="space-y-1">
              <label className="text-xs font-bold text-slate-300">Role</label>
              <select
                value={role}
                onChange={(e) => setRole(e.target.value)}
                className="w-full px-3 py-2.5 rounded-xl bg-slate-900 border border-white/10 text-white text-xs focus:border-blue-400 focus:outline-none"
              >
                <option value="customer">Customer Account</option>
                <option value="admin">Store Admin Account</option>
              </select>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="btn-glow w-full py-3.5 rounded-full font-bold text-xs text-white cursor-pointer shadow-lg mt-2"
          >
            {loading ? 'Authenticating...' : isLoginTab ? 'Sign In to Account' : 'Create Account'}
          </button>
        </form>

        {/* 1-Click Demo Login Presets */}
        <div className="mt-6 pt-4 border-t border-white/10 space-y-2">
          <div className="text-[10px] text-center text-slate-400 uppercase tracking-widest font-bold">
            1-Click Demo Presets
          </div>
          <div className="grid grid-cols-2 gap-2">
            <button
              type="button"
              onClick={fillDemoCustomer}
              className="glass-pill py-2 px-3 rounded-xl text-[11px] font-semibold text-slate-300 hover:text-white flex items-center justify-center space-x-1.5 cursor-pointer"
            >
              <User className="w-3.5 h-3.5 text-blue-400" />
              <span>Customer Demo</span>
            </button>
            <button
              type="button"
              onClick={fillDemoAdmin}
              className="glass-pill py-2 px-3 rounded-xl text-[11px] font-semibold text-blue-300 border-blue-500/30 hover:bg-blue-500/20 flex items-center justify-center space-x-1.5 cursor-pointer"
            >
              <Shield className="w-3.5 h-3.5 text-blue-400" />
              <span>Admin Demo</span>
            </button>
          </div>
        </div>

      </div>
    </div>
  );
};

export default AuthModal;
