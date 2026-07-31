import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { User, Lock, Mail, UserPlus, Sparkles, ArrowRight, Cpu, AlertCircle } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const RegisterPage = () => {
  const navigate = useNavigate();
  const { register } = useAuth();

  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [fieldErrors, setFieldErrors] = useState({});
  const [shake, setShake] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setFieldErrors({});
    setLoading(true);

    try {
      await register({ username, email, password, name, role: 'customer' });
      navigate('/products');
    } catch (err) {
      console.error('Registration error details:', err);
      if (err?.isNetworkError || (!err?.response && err?.name === 'AxiosError') || err?.message === 'Network Error' || err?.code === 'ERR_NETWORK') {
        setError('Unable to connect to backend server. Please ensure the Django server is running at http://localhost:8000.');
        setFieldErrors({});
      } else if (err?.response?.data && typeof err.response.data === 'object') {
        const data = err.response.data;
        setFieldErrors(data);
        const messages = [];
        Object.entries(data).forEach(([field, errList]) => {
          const detail = Array.isArray(errList) ? errList.join(' ') : String(errList);
          messages.push(`${field.toUpperCase()}: ${detail}`);
        });
        setError(messages.join(' | '));
      } else if (typeof err === 'object' && err !== null && !err.name) {
        setFieldErrors(err);
        const messages = [];
        Object.entries(err).forEach(([field, errList]) => {
          const detail = Array.isArray(errList) ? errList.join(' ') : String(errList);
          messages.push(detail);
        });
        setError(messages.join(' | '));
      } else {
        setError('Registration failed. Please check your credentials and try again.');
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
        className="grid grid-cols-1 lg:grid-cols-2 rounded-3xl overflow-hidden glass-panel border border-white/10 shadow-2xl min-h-[620px]"
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

          {/* Dark Gradient Overlay for Depth */}
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
              <span>JOIN THE NEXUS COMMUNITY</span>
            </div>
            <h2 className="text-3xl font-black text-white tracking-tight leading-tight drop-shadow-md">
              Create Your Account <br />
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-cyan-300 to-indigo-400">
                Unlock Quantum Tech
              </span>
            </h2>
            <p className="text-xs text-slate-300 leading-relaxed max-w-sm">
              Register now for express global dispatch, express order tracking, and member-only hardware drops.
            </p>
          </div>
        </div>

        {/* Right Half: Frosted Glass Registration Form */}
        <div className="flex flex-col justify-center p-6 md:p-12 relative z-10 space-y-5">
          <div className="space-y-1.5">
            <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-blue-500/10 text-blue-400 text-xs font-bold border border-blue-400/30">
              <UserPlus className="w-3.5 h-3.5" />
              <span>NEW ACCOUNT REGISTRATION</span>
            </div>
            <h1 className="text-3xl md:text-4xl font-black text-white tracking-tight">
              Create Account
            </h1>
            <p className="text-sm text-slate-300">
              Join the NEXUS quantum hardware ecosystem.
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
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {/* Full Name */}
              <div className="space-y-1.5">
                <label className="text-sm font-semibold text-slate-200">Full Name</label>
                <div className="relative">
                  <User className="w-4.5 h-4.5 text-slate-400 absolute left-3.5 top-3.5" />
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Alex Nexus"
                    required
                    className={`w-full pl-11 pr-4 py-3 rounded-xl bg-white/[0.04] border text-white text-sm focus:outline-none transition-all duration-300 placeholder:text-slate-500 ${
                      fieldErrors.name ? 'border-red-500/60 focus:ring-2 focus:ring-red-500/30' : 'border-white/10 focus:border-blue-400 focus:ring-2 focus:ring-blue-400/30'
                    }`}
                  />
                </div>
                {fieldErrors.name && (
                  <p className="text-xs text-red-400 flex items-center space-x-1 mt-1">
                    <AlertCircle className="w-3.5 h-3.5 shrink-0" />
                    <span>{Array.isArray(fieldErrors.name) ? fieldErrors.name.join(' ') : fieldErrors.name}</span>
                  </p>
                )}
              </div>

              {/* Email Address */}
              <div className="space-y-1.5">
                <label className="text-sm font-semibold text-slate-200">Email Address</label>
                <div className="relative">
                  <Mail className="w-4.5 h-4.5 text-slate-400 absolute left-3.5 top-3.5" />
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="alex@nexus.io"
                    required
                    className={`w-full pl-11 pr-4 py-3 rounded-xl bg-white/[0.04] border text-white text-sm focus:outline-none transition-all duration-300 placeholder:text-slate-500 ${
                      fieldErrors.email ? 'border-red-500/60 focus:ring-2 focus:ring-red-500/30' : 'border-white/10 focus:border-blue-400 focus:ring-2 focus:ring-blue-400/30'
                    }`}
                  />
                </div>
                {fieldErrors.email && (
                  <p className="text-xs text-red-400 flex items-center space-x-1 mt-1">
                    <AlertCircle className="w-3.5 h-3.5 shrink-0" />
                    <span>{Array.isArray(fieldErrors.email) ? fieldErrors.email.join(' ') : fieldErrors.email}</span>
                  </p>
                )}
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {/* Username */}
              <div className="space-y-1.5">
                <label className="text-sm font-semibold text-slate-200">Username</label>
                <div className="relative">
                  <User className="w-4.5 h-4.5 text-slate-400 absolute left-3.5 top-3.5" />
                  <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="username"
                    required
                    className={`w-full pl-11 pr-4 py-3 rounded-xl bg-white/[0.04] border text-white text-sm focus:outline-none transition-all duration-300 placeholder:text-slate-500 ${
                      fieldErrors.username ? 'border-red-500/60 focus:ring-2 focus:ring-red-500/30' : 'border-white/10 focus:border-blue-400 focus:ring-2 focus:ring-blue-400/30'
                    }`}
                  />
                </div>
                {fieldErrors.username && (
                  <p className="text-xs text-red-400 flex items-center space-x-1 mt-1">
                    <AlertCircle className="w-3.5 h-3.5 shrink-0" />
                    <span>{Array.isArray(fieldErrors.username) ? fieldErrors.username.join(' ') : fieldErrors.username}</span>
                  </p>
                )}
              </div>

              {/* Password */}
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
                    className={`w-full pl-11 pr-4 py-3 rounded-xl bg-white/[0.04] border text-white text-sm focus:outline-none transition-all duration-300 placeholder:text-slate-500 ${
                      fieldErrors.password ? 'border-red-500/60 focus:ring-2 focus:ring-red-500/30' : 'border-white/10 focus:border-blue-400 focus:ring-2 focus:ring-blue-400/30'
                    }`}
                  />
                </div>
                {fieldErrors.password && (
                  <p className="text-xs text-red-400 flex items-center space-x-1 mt-1">
                    <AlertCircle className="w-3.5 h-3.5 shrink-0" />
                    <span>{Array.isArray(fieldErrors.password) ? fieldErrors.password.join(' ') : fieldErrors.password}</span>
                  </p>
                )}
              </div>
            </div>

            {/* Submit Button with Spinner */}
            <button
              type="submit"
              disabled={loading}
              className="btn-glow w-full py-4 rounded-full font-bold text-sm text-white cursor-pointer shadow-xl flex items-center justify-center space-x-2 pt-2"
            >
              {loading ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  <span>Creating Account...</span>
                </>
              ) : (
                <>
                  <span>Register Account</span>
                  <ArrowRight className="w-4.5 h-4.5" />
                </>
              )}
            </button>
          </form>

          {/* Action Link: Sign In */}
          <div className="pt-4 border-t border-white/10 text-center text-sm text-slate-300">
            Already have an account?{' '}
            <Link to="/login" className="text-blue-400 font-bold hover:underline">
              Sign In Here
            </Link>
          </div>

        </div>
      </motion.div>
    </div>
  );
};

export default RegisterPage;
