import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Cpu, Smartphone, Tablet, Headphones, Watch, ShoppingBag, Star, Eye } from 'lucide-react';
import { useCart } from '../context/CartContext';

const getSpecIcon = (categoryName) => {
  switch (categoryName?.toLowerCase()) {
    case 'laptops':
      return Cpu;
    case 'phones':
      return Smartphone;
    case 'tablets':
      return Tablet;
    case 'audio':
      return Headphones;
    case 'accessories':
      return Watch;
    default:
      return Cpu;
  }
};

const getSpecText = (product) => {
  if (!product.specs) return 'High performance tech';
  if (product.specs.Processor) return product.specs.Processor;
  if (product.specs.processor) return product.specs.processor;
  if (product.specs.chip) return product.specs.chip;
  if (product.specs['Display Size']) return product.specs['Display Size'];
  if (product.specs.display) return product.specs.display;
  if (product.specs.camera) return product.specs.camera;
  if (product.specs.anc) return product.specs.anc;
  return Object.values(product.specs)[1] || Object.values(product.specs)[0] || 'Premium specifications';
};

const ProductCard = ({ product, onSelect, index = 0 }) => {
  const { addToCart } = useCart();
  const SpecIcon = getSpecIcon(product.category_name);
  const mainSpec = getSpecText(product);

  const [tilt, setTilt] = useState({ x: 0, y: 0 });

  const handleMouseMove = (e) => {
    const card = e.currentTarget.getBoundingClientRect();
    const width = card.width;
    const height = card.height;
    const mouseX = e.clientX - card.left;
    const mouseY = e.clientY - card.top;
    const rotateX = ((mouseY - height / 2) / height) * -12;
    const rotateY = ((mouseX - width / 2) / width) * 12;
    setTilt({ x: rotateX, y: rotateY });
  };

  const handleMouseLeave = () => {
    setTilt({ x: 0, y: 0 });
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-40px' }}
      transition={{ duration: 0.5, delay: (index % 4) * 0.08 }}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      style={{
        transform: `perspective(1000px) rotateX(${tilt.x}deg) rotateY(${tilt.y}deg)`,
        transition: tilt.x === 0 ? 'transform 0.5s ease' : 'none',
      }}
      onClick={() => onSelect(product)}
      className="glass-card rounded-2xl p-5 flex flex-col justify-between relative group cursor-pointer overflow-hidden border border-white/[0.06] hover:border-blue-400/40 shadow-xl"
    >
      {/* Top Badges: New / Featured */}
      <div className="flex items-center justify-between z-10">
        {product.is_new ? (
          <span className="px-3 py-1 rounded-full bg-blue-500/20 text-blue-300 text-xs font-extrabold uppercase tracking-wider border border-blue-400/30">
            NEW
          </span>
        ) : product.is_featured ? (
          <span className="px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 text-xs font-extrabold uppercase tracking-wider border border-indigo-400/30">
            FEATURED
          </span>
        ) : (
          <span className="text-xs font-semibold text-slate-400 tracking-wider uppercase">
            {product.brand}
          </span>
        )}

        <div className="flex items-center space-x-1 text-amber-400 text-sm font-semibold">
          <Star className="w-4 h-4 fill-amber-400" />
          <span>{product.rating || '4.8'}</span>
        </div>
      </div>

      {/* Product Image Forward Display */}
      <div className="relative h-52 w-full my-2 flex items-center justify-center overflow-hidden rounded-xl bg-white/[0.02]">
        <img
          src={product.image_url}
          alt={product.name}
          className="max-h-48 max-w-[90%] w-auto h-auto object-contain filter drop-shadow-[0_12px_20px_rgba(0,0,0,0.6)] group-hover:scale-105 transition-transform duration-500 ease-out"
          style={{ imageRendering: 'high-quality' }}
        />
        {/* Hover Quick View Overlay */}
        <div className="absolute inset-0 bg-blue-950/30 backdrop-blur-[2px] opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
          <span className="px-4.5 py-2 rounded-full glass-pill text-xs font-bold text-white flex items-center space-x-1.5 shadow-lg">
            <Eye className="w-4 h-4 text-blue-400" />
            <span>Quick Specs</span>
          </span>
        </div>
      </div>

      {/* Product Info */}
      <div className="space-y-2 pt-1 z-10">
        <h4 className="text-lg font-bold text-white tracking-wide line-clamp-1 group-hover:text-blue-300 transition-colors">
          {product.name}
        </h4>

        {/* Small Icon + One-line Spec */}
        <div className="flex items-center space-x-2 text-slate-300 text-sm py-0.5">
          <SpecIcon className="w-4 h-4 text-blue-400 shrink-0" />
          <span className="truncate font-medium">{mainSpec}</span>
        </div>

        {/* Dedicated Color Swatch Dots Bar */}
        {product.variants && product.variants.length > 0 && (
          <div className="flex items-center space-x-1.5 py-1" title={`${product.variants.length} colors available`}>
            <span className="text-[10px] text-slate-400 font-extrabold uppercase tracking-wider">Colors:</span>
            <div className="flex items-center space-x-1.5">
              {product.variants.slice(0, 5).map((v) => (
                <span
                  key={v.id}
                  className="w-3.5 h-3.5 rounded-full border border-white/40 shadow-sm shrink-0 inline-block transition-transform hover:scale-125 cursor-pointer"
                  style={{ backgroundColor: v.hex_code }}
                  title={v.color_name}
                />
              ))}
              {product.variants.length > 5 && (
                <span className="text-[10px] text-slate-400 font-bold">+{product.variants.length - 5}</span>
              )}
            </div>
          </div>
        )}

        {/* Footer: Price & Add to Cart Button */}
        <div className="flex items-center justify-between pt-2.5 border-t border-white/5">
          <div className="flex flex-col">
            <span className="text-xs text-slate-400 uppercase font-semibold">Price</span>
            <span className="text-xl font-black text-white">
              ${parseFloat(product.price).toFixed(2)}
            </span>
          </div>

          <button
            onClick={(e) => {
              e.stopPropagation();
              const defaultVariant = product.variants?.find(v => v.is_default) || product.variants?.[0] || null;
              addToCart(product, 1, defaultVariant);
            }}
            className="btn-glow p-3 rounded-xl text-white flex items-center justify-center cursor-pointer hover:scale-105 transition-transform"
            title="Add to Cart"
          >
            <ShoppingBag className="w-4.5 h-4.5" />
          </button>
        </div>
      </div>
    </motion.div>
  );
};

export default ProductCard;
