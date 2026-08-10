import React, { useState } from 'react';
import { X, Star, ShoppingBag, ShieldCheck, Truck, RefreshCw, Cpu, Check } from 'lucide-react';
import { useCart } from '../context/CartContext';

/**
 * ProductDetailModal Component:
 * Interactive modal rendering comprehensive hardware specs, variant color selectors,
 * quantity toggles, and direct add-to-cart action.
 */
const ProductDetailModal = ({ product, onClose }) => {
  const { addToCart } = useCart();
  const [quantity, setQuantity] = useState(1);
  const [added, setAdded] = useState(false);

  const defaultVariant = product?.variants?.find(v => v.is_default) || product?.variants?.[0] || null;
  const [selectedVariant, setSelectedVariant] = useState(defaultVariant);

  React.useEffect(() => {
    const def = product?.variants?.find(v => v.is_default) || product?.variants?.[0] || null;
    setSelectedVariant(def);
  }, [product]);

  if (!product) return null;

  const currentPrice = parseFloat(product.price) + (selectedVariant?.price_delta ? parseFloat(selectedVariant.price_delta) : 0);
  const activeImage = selectedVariant?.image_url || product.image_url;
  const activeStock = selectedVariant ? selectedVariant.stock_qty : product.stock_qty;
  const isOutOfStock = activeStock <= 0;

  const handleAddToCart = () => {
    addToCart(product, quantity, selectedVariant);
    setAdded(true);
    setTimeout(() => setAdded(false), 2000);
  };

  const specsList = product.specs ? Object.entries(product.specs) : [];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-fade-in overflow-y-auto">
      <div className="relative w-full max-w-4xl glass-panel rounded-3xl p-6 md:p-8 my-8 shadow-2xl border border-white/10 text-slate-100 max-h-[90vh] overflow-y-auto no-scrollbar" data-lenis-prevent="true">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-6 right-6 p-2 rounded-full glass-pill text-slate-400 hover:text-white hover:border-blue-400/50 cursor-pointer transition-colors z-20"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="grid grid-cols-1 md:grid-cols-12 gap-8 items-start">
          {/* Left Column: Image Showcase */}
          <div className="md:col-span-6 flex flex-col items-center">
            <div className="relative w-full h-80 bg-white/[0.03] rounded-2xl p-6 flex items-center justify-center border border-white/5 overflow-hidden">
              <div className="absolute inset-0 bg-blue-500/10 blur-3xl rounded-full" />
              <img
                src={activeImage}
                alt={product.name}
                className="max-h-72 max-w-full object-contain filter drop-shadow-[0_20px_30px_rgba(0,0,0,0.7)] hover:scale-105 transition-transform duration-500"
              />
            </div>
            
            {/* Guarantee badges */}
            <div className="grid grid-cols-3 gap-3 w-full mt-4 text-center">
              <div className="glass-pill p-2.5 rounded-xl flex flex-col items-center text-[11px] text-slate-300">
                <ShieldCheck className="w-4 h-4 text-blue-400 mb-1" />
                <span>2-Yr Warranty</span>
              </div>
              <div className="glass-pill p-2.5 rounded-xl flex flex-col items-center text-[11px] text-slate-300">
                <Truck className="w-4 h-4 text-cyan-400 mb-1" />
                <span>Free Express</span>
              </div>
              <div className="glass-pill p-2.5 rounded-xl flex flex-col items-center text-[11px] text-slate-300">
                <RefreshCw className="w-4 h-4 text-indigo-400 mb-1" />
                <span>30-Day Return</span>
              </div>
            </div>
          </div>

          {/* Right Column: Spec & Details */}
          <div className="md:col-span-6 space-y-5">
            {/* Header info */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="px-3 py-1 rounded-full bg-blue-500/10 text-blue-400 text-xs font-bold uppercase tracking-wider border border-blue-400/20">
                  {product.category_name} • {product.brand}
                </span>
                <div className="flex items-center space-x-1 text-amber-400 text-sm font-semibold">
                  <Star className="w-4 h-4 fill-amber-400" />
                  <span>{product.rating}</span>
                </div>
              </div>
              <h2 className="text-2xl md:text-3xl font-extrabold text-white tracking-wide">
                {product.name}
              </h2>
              <div className="text-2xl font-black text-blue-400 mt-2">
                ${currentPrice.toFixed(2)}
              </div>
            </div>

            {/* Description */}
            <p className="text-sm text-slate-300 leading-relaxed font-normal">
              {product.description}
            </p>

            {/* Apple-Style Color Variant Swatch Selector */}
            {product.variants && product.variants.length > 0 && (
              <div className="space-y-2 pt-1 border-t border-white/5">
                <div className="flex items-center justify-between">
                  <span className="text-xs text-slate-400 font-bold uppercase tracking-wider">
                    Color: <span className="text-white font-extrabold">{selectedVariant?.color_name}</span>
                  </span>
                  {selectedVariant?.price_delta != 0 && (
                    <span className="text-xs font-semibold text-blue-400">
                      {parseFloat(selectedVariant.price_delta) > 0 ? `+$${parseFloat(selectedVariant.price_delta).toFixed(2)}` : `-$${Math.abs(selectedVariant.price_delta).toFixed(2)}`}
                    </span>
                  )}
                </div>
                <div className="flex items-center space-x-2.5 pt-0.5">
                  {product.variants.map((variant) => {
                    const isSelected = selectedVariant?.id === variant.id;
                    return (
                      <button
                        key={variant.id}
                        type="button"
                        onClick={() => setSelectedVariant(variant)}
                        aria-label={variant.color_name}
                        title={`${variant.color_name}${parseFloat(variant.price_delta) !== 0 ? ` (${parseFloat(variant.price_delta) > 0 ? '+' : ''}$${variant.price_delta})` : ''}`}
                        className={`w-8 h-8 rounded-full border-2 transition-all cursor-pointer flex items-center justify-center ${
                          isSelected
                            ? 'border-blue-400 scale-110 shadow-lg shadow-blue-500/30 ring-2 ring-blue-400/20'
                            : 'border-white/20 hover:border-white/50 hover:scale-105'
                        }`}
                        style={{ backgroundColor: variant.hex_code }}
                      >
                        {isSelected && (
                          <span className={`w-2 h-2 rounded-full ${parseInt(variant.hex_code.replace('#',''), 16) > 0x888888 ? 'bg-black' : 'bg-white'}`} />
                        )}
                      </button>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Detailed Specs Table */}
            {specsList.length > 0 && (
              <div className="space-y-2">
                <h4 className="text-xs uppercase tracking-widest text-slate-400 font-bold flex items-center space-x-1.5">
                  <Cpu className="w-3.5 h-3.5 text-blue-400" />
                  <span>Technical Specifications</span>
                </h4>
                <div className="grid grid-cols-2 gap-2 bg-white/[0.03] p-3 rounded-2xl border border-white/5">
                  {specsList.map(([key, val]) => (
                    <div key={key} className="flex flex-col text-xs">
                      <span className="text-slate-400 uppercase text-[10px] font-semibold tracking-wider">
                        {key}
                      </span>
                      <span className="text-slate-200 font-bold capitalize">
                        {val}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Stock indicator */}
            <div className="flex items-center space-x-2 text-xs">
              <span className={`w-2.5 h-2.5 rounded-full ${!isOutOfStock ? 'bg-emerald-400 animate-pulse' : 'bg-red-400'}`} />
              <span className="text-slate-300 font-medium">
                {!isOutOfStock
                  ? `In Stock (${activeStock} units available${selectedVariant ? ' in ' + selectedVariant.color_name : ''})`
                  : `Out of Stock${selectedVariant ? ' in ' + selectedVariant.color_name : ''}`}
              </span>
            </div>

            {/* Quantity & Add to Cart Controls */}
            <div className="flex items-center space-x-4 pt-4 border-t border-white/10">
              <div className="flex items-center glass-pill rounded-full border-white/10">
                <button
                  onClick={() => setQuantity(Math.max(1, quantity - 1))}
                  className="px-3 py-2 text-slate-300 hover:text-white font-bold cursor-pointer"
                >
                  -
                </button>
                <span className="px-4 text-sm font-bold text-white">{quantity}</span>
                <button
                  onClick={() => setQuantity(quantity + 1)}
                  className="px-3 py-2 text-slate-300 hover:text-white font-bold cursor-pointer"
                >
                  +
                </button>
              </div>

              <button
                onClick={handleAddToCart}
                disabled={isOutOfStock}
                className={`flex-1 py-3.5 px-6 rounded-full font-bold text-sm text-white flex items-center justify-center space-x-2 transition-all cursor-pointer ${
                  added 
                    ? 'bg-emerald-500 shadow-lg shadow-emerald-500/30' 
                    : isOutOfStock
                    ? 'bg-slate-700/50 cursor-not-allowed text-slate-400 border border-white/5'
                    : 'btn-glow'
                }`}
              >
                {added ? (
                  <>
                    <Check className="w-4 h-4 text-white" />
                    <span>Added to Cart!</span>
                  </>
                ) : isOutOfStock ? (
                  <span>Out of stock in this color</span>
                ) : (
                  <>
                    <ShoppingBag className="w-4 h-4" />
                    <span>Add to Cart (${(currentPrice * quantity).toFixed(2)})</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductDetailModal;
