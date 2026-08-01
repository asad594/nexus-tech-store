import React, { useState } from 'react';
import { useNavigate, useSearchParams, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { User, Lock, Sparkles, KeyRound, ArrowRight, Cpu } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const LoginPage = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const rawRedirect = searchParams.get('redirect') || '/products';
  const redirect = rawRedirect.startsWith('/') ? rawRedirect : `/${rawRedirect}`;

  const { login } = useAuth();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [shake, setShake] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      await login(username, password);
      navigate(redirect);
    } catch (err) {
      console.error('Login error', err);
      if (err?.code === 'ERR_NETWORK' || !err?.response || err?.response?.status >= 500) {
        setError('Unable to connect to backend server. Please ensure the Django backend server is running at http://localhost:8000.');
      } else if (err?.response?.status === 401) {
        setError('Invalid username or password. Please try again.');
      } else {
        setError(err?.response?.data?.error || err?.response?.data?.detail || 'Authentication failed. Please verify credentials.');
      }
      setShake(true);
      setTimeout(() => setShake(false), 500);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 md:py-12">
      <motion.div
        animate={shake ? { x: [-10, 10, -10, 10, 0] } : {}}
        transition={{ duration: 0.4 }}
        className="grid grid-cols-1 lg:grid-cols-2 rounded-3xl overflow-hidden glass-panel border border-white/10 shadow-2xl min-h-[600px]"
      >
        {/* Left Half: Ambient Video & Brand Showcase */}
        <div className="relative h-56 lg:h-full w-full overflow-hidden bg-black flex flex-col justify-between p-6 lg:p-12">
          {/* Ambient Looping Video */}
          <video
            autoPlay
            loop
            muted
            playsInline
            preload="auto"
            src="/videos/Glowing_sphere_with_orbiting_par.mp4"
            className="absolute inset-0 w-full h-full object-cover object-center filter brightness-90 contrast-105"
          />

          {/* Dark Gradient Overlay */}
          <div className="absolute inset-0 bg-gradient-to-t from-[#07070b] via-[#07070b]/40 to-transparent pointer-events-none" />
          <div className="absolute inset-0 bg-blue-900/10 pointer-events-none" />

          {/* Top Brand Logo */}
          <div className="relative z-10 flex items-center space-x-3">
            <div className="w-10 h-10 rounded-2xl bg-gradient-blue flex items-center justify-center text-white shadow-[0_0_20px_rgba(77,166,255,0.5)]">
              <Cpu className="w-5 h-5" />
            </div>
            <span className="text-xl font-black text-white tracking-widest">NEXUS</span>
          </div>

          {/* Bottom Hero Tagline */}
          <div className="relative z-10 space-y-2 hidden lg:block">
            <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full glass-pill border-blue-400/40 text-blue-300 text-[11px] font-bold tracking-wider">
              <Sparkles className="w-3.5 h-3.5 text-blue-400" />
              <span>QUANTUM HARDWARE AUTHENTICATION</span>
            </div>
            <h2 className="text-3xl font-black text-white tracking-tight leading-tight drop-shadow-md">
              Enter the Realm of <br />
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-cyan-300 to-indigo-400">
                Next-Gen Electronics
              </span>
            </h2>
            <p className="text-xs text-slate-300 leading-relaxed max-w-sm">
              Sign in to unlock personalized hardware configurations, order history, and exclusive dispatches.
            </p>
          </div>
        </div>

        {/* Right Half: Frosted Glass Form Container */}
        <div className="flex flex-col justify-center p-6 md:p-12 relative z-10 space-y-6">
          <div className="space-y-2">
            <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-blue-500/10 text-blue-400 text-xs font-bold border border-blue-400/30">
              <KeyRound className="w-3.5 h-3.5" />
              <span>WELCOME BACK</span>
            </div>
            <h1 className="text-3xl md:text-4xl font-black text-white tracking-tight">
              Sign In to Account
            </h1>
            <p className="text-sm text-slate-300">
              Access your quantum cart, order status, and customer dashboard.
            </p>
          </div>

          {error && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-sm font-medium text-center shadow-lg"
            >
              {error}
            </motion.div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Username Input */}
            <div className="space-y-1.5">
              <label className="text-sm font-semibold text-slate-200">Username or Email</label>
              <div className="relative">
                <User className="w-4.5 h-4.5 text-slate-400 absolute left-3.5 top-3.5" />
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="enter username"
                  required
                  className="w-full pl-11 pr-4 py-3 rounded-xl bg-white/[0.04] border border-white/10 text-white text-sm focus:border-blue-400 focus:ring-2 focus:ring-blue-400/30 transition-all duration-300 focus:outline-none placeholder:text-slate-500"
                />
              </div>
            </div>

            {/* Password Input */}
            <div className="space-y-1.5">
              <label className="text-sm font-semibold text-slate-200">Password</label>
              <div className="relative">
                <Lock className="w-4.5 h-4.5 text-slate-400 absolute left-3.5 top-3.5" />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  required
                  className="w-full pl-11 pr-4 py-3 rounded-xl bg-white/[0.04] border border-white/10 text-white text-sm focus:border-blue-400 focus:ring-2 focus:ring-blue-400/30 transition-all duration-300 focus:outline-none placeholder:text-slate-500"
                />
              </div>
            </div>

            {/* Submit Button with Loading Spinner */}
            <button
              type="submit"
              disabled={loading}
              className="btn-glow w-full py-4 rounded-full font-bold text-sm text-white cursor-pointer shadow-xl flex items-center justify-center space-x-2"
            >
              {loading ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  <span>Authenticating...</span>
                </>
              ) : (
                <>
                  <span>Sign In to Account</span>
                  <ArrowRight className="w-4.5 h-4.5" />
                </>
              )}
            </button>
          </form>

          {/* Action Link: Register */}
          <div className="pt-4 border-t border-white/10 text-center text-sm text-slate-300">
            Don't have an account?{' '}
            <Link to="/register" className="text-blue-400 font-bold hover:underline">
              Register Here
            </Link>
          </div>

        </div>
      </motion.div>
    </div>
  );
};

export default LoginPage;
