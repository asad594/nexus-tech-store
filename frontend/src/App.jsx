import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { CartProvider } from './context/CartContext';
import { LenisProvider } from './context/LenisContext';
import Navbar from './components/Navbar';
import HomePage from './pages/HomePage';
import ProductsPage from './pages/ProductsPage';
import ProductDetailPage from './pages/ProductDetailPage';
import CartPage from './pages/CartPage';
import CheckoutPage from './pages/CheckoutPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import AdminPage from './pages/AdminPage';
import OrdersPage from './pages/OrdersPage';
import { Cpu } from 'lucide-react';

function Layout() {
  return (
    <div className="bg-ambient-grid min-h-screen relative text-slate-100 selection:bg-blue-500 selection:text-white flex flex-col justify-between">
      
      {/* Global Ambient Looping Background Video */}
      <div className="fixed inset-0 z-[-20] overflow-hidden pointer-events-none">
        <video
          autoPlay
          loop
          muted
          playsInline
          preload="auto"
          src="/videos/Bokeh_light_orbs_floating_upward.mp4"
          className="w-full h-full object-cover object-center opacity-20 filter brightness-90 contrast-110"
        />
        {/* Solid Dark Overlay for Strong Readability */}
        <div className="absolute inset-0 bg-[#07070b]/40 pointer-events-none" />
      </div>

      {/* Background Ambient Glows */}
      <div className="ambient-shape-1" />
      <div className="ambient-shape-2" />

      <div className="relative z-10">
        {/* Navigation Bar */}
        <Navbar />

        {/* Dynamic Route Pages */}
        <div className="pb-16">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/products" element={<ProductsPage />} />
            <Route path="/products/:id" element={<ProductDetailPage />} />
            <Route path="/cart" element={<CartPage />} />
            <Route path="/checkout" element={<CheckoutPage />} />
            <Route path="/orders" element={<OrdersPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/admin" element={<AdminPage />} />
          </Routes>
        </div>
      </div>

      {/* Footer */}
      <footer className="max-w-7xl mx-auto px-4 md:px-8 pt-16 border-t border-white/10 mt-16 text-slate-400 text-xs w-full">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 pb-12">
          <div className="space-y-3">
            <div className="flex items-center space-x-2">
              <div className="w-7 h-7 rounded-full bg-gradient-blue flex items-center justify-center text-white">
                <Cpu className="w-4 h-4" />
              </div>
              <span className="text-lg font-bold text-white tracking-wider">NEXUS</span>
            </div>
            <p className="text-slate-400 text-xs leading-relaxed">
              Premium futuristic electronics store featuring frosted glass aesthetics and scroll-scrubbed video hardware showcases.
            </p>
          </div>

          <div>
            <h4 className="text-white font-bold mb-3 uppercase tracking-wider text-[11px]">Quick Links</h4>
            <ul className="space-y-2">
              <li><a href="/products?category=Laptops" className="hover:text-blue-400 transition-colors">Quantum Laptops</a></li>
              <li><a href="/products?category=Phones" className="hover:text-blue-400 transition-colors">Flagship Phones</a></li>
              <li><a href="/products?category=Tablets" className="hover:text-blue-400 transition-colors">Digital Tablets</a></li>
              <li><a href="/products?category=Audio" className="hover:text-blue-400 transition-colors">Spatial Audio</a></li>
              <li><a href="/products?category=Accessories" className="hover:text-blue-400 transition-colors">Cyber Accessories</a></li>
            </ul>
          </div>

          <div>
            <h4 className="text-white font-bold mb-3 uppercase tracking-wider text-[11px]">Quantum Care</h4>
            <ul className="space-y-2">
              <li><span className="hover:text-blue-400 transition-colors cursor-pointer">24/7 Priority Support</span></li>
              <li><span className="hover:text-blue-400 transition-colors cursor-pointer">Express Dispatch</span></li>
              <li><span className="hover:text-blue-400 transition-colors cursor-pointer">Global Warranty</span></li>
              <li><span className="hover:text-blue-400 transition-colors cursor-pointer">30-Day Returns</span></li>
            </ul>
          </div>

          <div className="space-y-3">
            <h4 className="text-white font-bold uppercase tracking-wider text-[11px]">Newsletter</h4>
            <p className="text-xs text-slate-400">Receive instant updates for hardware drops.</p>
            <div className="flex space-x-2">
              <input
                type="email"
                placeholder="enter email..."
                className="px-3 py-2 rounded-full bg-white/[0.04] border border-white/10 text-white text-xs w-full focus:outline-none"
              />
              <button className="btn-glow px-4 py-2 rounded-full font-bold text-white text-xs cursor-pointer">
                Join
              </button>
            </div>
          </div>
        </div>

        <div className="text-center pt-8 border-t border-white/5 text-slate-500 pb-8">
          © {new Date().getFullYear()} NEXUS Electronics Inc. All rights reserved. Glassmorphism Design System.
        </div>
      </footer>

    </div>
  );
}

export default function App() {
  return (
    <Router>
      <LenisProvider>
        <AuthProvider>
          <CartProvider>
            <Layout />
          </CartProvider>
        </AuthProvider>
      </LenisProvider>
    </Router>
  );
}

