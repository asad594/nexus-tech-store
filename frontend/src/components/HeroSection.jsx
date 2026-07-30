import React, { useState } from 'react';
import { Sparkles, ArrowRight, ShieldCheck, Zap, Cpu, Award } from 'lucide-react';
import { motion } from 'framer-motion';

const HeroSection = ({ onExploreClick, featuredProduct, onSelectProduct }) => {
  const [rotate, setRotate] = useState({ x: 0, y: 0 });

  const handleMouseMove = (e) => {
    const card = e.currentTarget.getBoundingClientRect();
    const boxWidth = card.width;
    const boxHeight = card.height;
    const mouseX = e.clientX - card.left;
    const mouseY = e.clientY - card.top;
    const rotateX = ((mouseY - boxHeight / 2) / boxHeight) * -15;
    const rotateY = ((mouseX - boxWidth / 2) / boxWidth) * 15;
    setRotate({ x: rotateX, y: rotateY });
  };

  const handleMouseLeave = () => {
    setRotate({ x: 0, y: 0 });
  };

  return (
    <section className="relative py-12 md:py-20 px-4 md:px-8 max-w-7xl mx-auto overflow-hidden">
      {/* Background ambient lighting */}
      <div className="ambient-shape-1" />
      <div className="ambient-shape-2" />

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
        {/* Left Column: Copy & CTAs */}
        <motion.div 
          initial={{ opacity: 0, x: -30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.8 }}
          className="lg:col-span-7 space-y-6 text-center lg:text-left z-10"
        >
          {/* Badge */}
          <div className="inline-flex items-center space-x-2 px-4 py-1.5 rounded-full glass-pill border-blue-500/30 text-blue-400 text-xs font-semibold tracking-wide">
            <Sparkles className="w-3.5 h-3.5 animate-spin" />
            <span>NEXUS 2026 QUANTUM COLLECTION</span>
          </div>

          {/* Heading */}
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-black tracking-tight text-white leading-[1.1]">
            THE FUTURE OF <br />
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-cyan-300 to-indigo-400 text-glow">
              NEXT-GEN TECH
            </span>
          </h1>

          {/* Subtitle */}
          <p className="text-slate-400 text-base md:text-lg max-w-xl mx-auto lg:mx-0 font-normal leading-relaxed">
            Architected with precision glassmorphic aesthetics, ultra-quantum processors, 
            and aerospace materials designed to elevate your digital experience.
          </p>

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center lg:justify-start space-y-4 sm:space-y-0 sm:space-x-4 pt-4">
            <button
              onClick={onExploreClick}
              className="btn-glow px-8 py-4 rounded-full text-sm font-bold text-white flex items-center space-x-3 w-full sm:w-auto justify-center cursor-pointer group"
            >
              <span>Explore Products</span>
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </button>
            
            {featuredProduct && (
              <button
                onClick={() => onSelectProduct(featuredProduct)}
                className="glass-pill px-8 py-4 rounded-full text-sm font-semibold text-slate-200 hover:text-white hover:border-blue-400/50 w-full sm:w-auto justify-center cursor-pointer"
              >
                View Flagship Specs
              </button>
            )}
          </div>

          {/* Key Metrics */}
          <div className="grid grid-cols-3 gap-6 pt-8 border-t border-white/10 max-w-md mx-auto lg:mx-0">
            <div>
              <div className="text-2xl font-bold text-white">4.9★</div>
              <div className="text-xs text-slate-400 mt-0.5">Customer Score</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-blue-400">100%</div>
              <div className="text-xs text-slate-400 mt-0.5">Authentic Specs</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-cyan-300">24/7</div>
              <div className="text-xs text-slate-400 mt-0.5">Express Dispatch</div>
            </div>
          </div>
        </motion.div>

        {/* Right Column: 3D-Tilted Floating Glass Showcase Panel */}
        <motion.div 
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.9, delay: 0.2 }}
          className="lg:col-span-5 flex justify-center z-10"
        >
          <div
            onMouseMove={handleMouseMove}
            onMouseLeave={handleMouseLeave}
            style={{
              transform: `perspective(1000px) rotateX(${rotate.x}deg) rotateY(${rotate.y}deg)`,
              transition: rotate.x === 0 ? 'transform 0.5s ease' : 'none'
            }}
            className="w-full max-w-md glass-panel rounded-3xl p-6 relative cursor-pointer group shadow-[0_25px_60px_-15px_rgba(0,0,0,0.8)]"
            onClick={() => featuredProduct && onSelectProduct(featuredProduct)}
          >
            {/* Top Badge */}
            <div className="flex items-center justify-between mb-4">
              <span className="px-3 py-1 rounded-full bg-blue-500/20 text-blue-300 text-[11px] font-bold uppercase tracking-wider border border-blue-400/30">
                Flagship Edition
              </span>
              <div className="flex items-center space-x-1 text-amber-400 text-xs font-bold">
                <Award className="w-4 h-4" />
                <span>Top Pick 2026</span>
              </div>
            </div>

            {/* Product Image Floating on Glass Panel */}
            <div className="relative h-64 w-full flex items-center justify-center my-4 overflow-hidden rounded-2xl bg-gradient-to-b from-white/5 to-transparent border border-white/5">
              <div className="absolute inset-0 bg-blue-500/10 blur-2xl rounded-full group-hover:bg-blue-500/20 transition-colors" />
              <img
                src={featuredProduct?.image_url || 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?q=80&w=1000'}
                alt={featuredProduct?.name || 'Flagship Device'}
                className="max-h-56 max-w-full object-contain relative z-10 filter drop-shadow-[0_15px_25px_rgba(0,0,0,0.7)] group-hover:scale-105 transition-transform duration-500"
              />
            </div>

            {/* Product Info */}
            <div className="space-y-3 pt-2">
              <div className="flex items-center justify-between">
                <h3 className="text-xl font-bold text-white tracking-wide">
                  {featuredProduct?.name || 'NexusBook Pro X16'}
                </h3>
                <span className="text-lg font-extrabold text-blue-400">
                  ${featuredProduct?.price || '2,499.00'}
                </span>
              </div>

              {/* Specs Badge */}
              <div className="flex items-center space-x-2 text-slate-300 text-xs bg-white/5 px-3 py-2 rounded-xl border border-white/5">
                <Cpu className="w-4 h-4 text-blue-400 shrink-0" />
                <span className="truncate">
                  {featuredProduct?.specs?.chip || 'Quantum M3 Max • 36GB RAM • 1TB NVMe'}
                </span>
              </div>
            </div>

            {/* Glowing Accent Ring on Hover */}
            <div className="absolute -inset-0.5 rounded-3xl bg-gradient-to-r from-blue-500/0 via-blue-400/20 to-blue-500/0 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none blur-sm" />
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default HeroSection;
