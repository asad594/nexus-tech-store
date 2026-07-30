import React, { useState, useEffect } from 'react';
import { Link, NavLink, useNavigate, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  Cpu, ShoppingBag, User, Shield, Laptop, Smartphone, 
  Tablet, Headphones, Watch, Sparkles, LogOut, Package 
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useCart } from '../context/CartContext';
import API from '../api';

const categoryIcons = {
  'All': Sparkles,
  'Laptops': Laptop,
  'Phones': Smartphone,
  'Tablets': Tablet,
  'Audio': Headphones,
  'Accessories': Watch,
};

const Navbar = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuth();
  const { totalItems } = useCart();
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    const fetchCat = async () => {
      try {
        const res = await API.get('/categories/');
        setCategories(res.data);
      } catch (err) {
        console.error('Failed to fetch navbar categories', err);
      }
    };
    fetchCat();
  }, []);

  const searchParams = new URLSearchParams(location.search);
  const activeCategory = searchParams.get('category') || 'All';
  const allCategoryNames = ['All', ...(categories.map(c => c.name))];

  return (
    <header className="sticky top-4 z-40 px-4 md:px-8 max-w-7xl mx-auto space-y-3">
      {/* Primary Floating Glass Navbar Pill */}
      <nav className="glass-panel rounded-full px-6 py-3 flex items-center justify-between shadow-2xl transition-all duration-300">
        
        {/* Brand Logo */}
        <Link to="/" className="flex items-center space-x-3 group cursor-pointer">
          <div className="w-10 h-10 rounded-full bg-gradient-blue flex items-center justify-center shadow-lg shadow-blue-500/30 group-hover:scale-105 transition-transform duration-300">
            <Cpu className="w-5 h-5 text-white animate-pulse" />
          </div>
          <div className="flex flex-col text-left">
            <span className="text-xl font-extrabold tracking-wider bg-clip-text text-transparent bg-gradient-to-r from-white via-slate-200 to-blue-400">
              NEXUS
            </span>
            <span className="text-[9px] uppercase tracking-widest text-blue-400 font-semibold -mt-1">
              Next-Gen Tech
            </span>
          </div>
        </Link>

        {/* Primary Nav Links */}
        <div className="hidden md:flex items-center space-x-1 lg:space-x-2 bg-white/[0.03] p-1 rounded-full border border-white/5">
          <NavLink 
            to="/" 
            end
            className={({ isActive }) => 
              `px-5 py-2 text-sm font-semibold rounded-full transition-colors ${
                isActive ? 'bg-blue-500/20 text-blue-300 border border-blue-400/40' : 'text-slate-300 hover:text-white'
              }`
            }
          >
            Home
          </NavLink>
          <NavLink 
            to="/products" 
            className={({ isActive }) => 
              `px-5 py-2 text-sm font-semibold rounded-full transition-colors ${
                isActive ? 'bg-blue-500/20 text-blue-300 border border-blue-400/40' : 'text-slate-300 hover:text-white'
              }`
            }
          >
            Products
          </NavLink>
        </div>

        {/* Right Actions: Cart & Auth */}
        <div className="flex items-center space-x-3">
          {/* Cart Trigger */}
          <Link
            to="/cart"
            className="relative glass-pill px-4 py-2.5 rounded-full flex items-center space-x-2 text-slate-200 hover:text-white hover:border-blue-400/50 cursor-pointer"
          >
            <ShoppingBag className="w-4.5 h-4.5 text-blue-400" />
            <span className="text-sm font-semibold">Cart</span>
            {totalItems > 0 && (
              <span className="w-5 h-5 rounded-full bg-blue-500 text-white text-xs font-bold flex items-center justify-center shadow-md shadow-blue-500/50">
                {totalItems}
              </span>
            )}
          </Link>

          {/* User Auth or Admin Dashboard Link */}
          {user ? (
            <div className="flex items-center space-x-2">
              <Link
                to="/orders"
                className="glass-pill px-3 py-2 rounded-full flex items-center space-x-1 text-xs font-semibold text-slate-200 hover:text-white hover:border-blue-400/50 cursor-pointer"
                title="My Orders"
              >
                <Package className="w-4 h-4 text-blue-400" />
                <span className="hidden sm:inline">Orders</span>
              </Link>
              {user.role === 'admin' && (
                <Link
                  to="/admin"
                  className="glass-pill px-3.5 py-2 rounded-full flex items-center space-x-1.5 text-sm font-semibold text-blue-300 border-blue-500/40 hover:bg-blue-500/20 cursor-pointer"
                >
                  <Shield className="w-4 h-4 text-blue-400" />
                  <span className="hidden sm:inline">Admin</span>
                </Link>
              )}
              <div className="glass-pill px-3.5 py-2 rounded-full flex items-center space-x-2 border-white/10">
                <div className="w-6.5 h-6.5 rounded-full bg-blue-600/40 flex items-center justify-center text-xs font-bold text-blue-300">
                  {user.name ? user.name[0].toUpperCase() : 'U'}
                </div>
                <span className="text-sm font-medium text-slate-200 hidden sm:inline max-w-[110px] truncate">
                  {user.name || user.username}
                </span>
                <button 
                  onClick={logout} 
                  title="Logout" 
                  className="text-slate-400 hover:text-red-400 transition-colors p-1 cursor-pointer"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            </div>
          ) : (
            <Link
              to="/login"
              className="btn-glow px-6 py-2.5 rounded-full text-sm font-bold text-white flex items-center space-x-2 cursor-pointer"
            >
              <User className="w-4 h-4" />
              <span>Sign In</span>
            </Link>
          )}
        </div>
      </nav>

      {/* Secondary Category Filter Row with Sliding Glow Background */}
      <div className="flex items-center justify-center overflow-x-auto no-scrollbar py-1 space-x-2 relative">
        {allCategoryNames.map((catName) => {
          const IconComponent = categoryIcons[catName] || Sparkles;
          const isActive = location.pathname === '/products' && activeCategory === catName;

          return (
            <button
              key={catName}
              onClick={() => {
                if (catName === 'All') {
                  navigate('/products');
                } else {
                  navigate(`/products?category=${catName}`);
                }
              }}
              className="relative px-4.5 py-2 rounded-full text-sm font-semibold flex items-center space-x-2 transition-colors whitespace-nowrap cursor-pointer z-10"
            >
              {/* Sliding Active Glass Glow Pill Background */}
              {isActive && (
                <motion.div
                  layoutId="activeCategoryPill"
                  className="absolute inset-0 rounded-full bg-blue-500/20 border border-blue-400/50 shadow-[0_0_15px_rgba(77,166,255,0.4)] z-0"
                  transition={{ type: 'spring', stiffness: 350, damping: 30 }}
                />
              )}

              <IconComponent className={`w-4 h-4 z-10 ${isActive ? 'text-blue-300 animate-pulse' : 'text-slate-400'}`} />
              <span className={`z-10 ${isActive ? 'text-white font-bold' : 'text-slate-300 hover:text-white'}`}>
                {catName}
              </span>
            </button>
          );
        })}
      </div>
    </header>
  );
};

export default Navbar;
