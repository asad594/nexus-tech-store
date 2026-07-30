import React from 'react';
import { useNavigate } from 'react-router-dom';
import { X, Trash2, ShoppingBag, ArrowRight, Sparkles } from 'lucide-react';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';

const CartDrawer = ({ onProceedToCheckout }) => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const { 
    cartItems, 
    isCartOpen, 
    setIsCartOpen, 
    updateQuantity, 
    removeFromCart, 
    subtotal, 
    totalItems 
  } = useCart();

  if (!isCartOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-hidden">
      {/* Backdrop */}
      <div 
        onClick={() => setIsCartOpen(false)} 
        className="absolute inset-0 bg-black/70 backdrop-blur-sm transition-opacity" 
      />

      <div className="fixed inset-y-0 right-0 max-w-full flex pl-10">
        <div className="w-screen max-w-md glass-panel p-6 shadow-2xl border-l border-white/10 flex flex-col justify-between text-slate-100 animate-slide-left">
          
          {/* Header */}
          <div className="flex items-center justify-between pb-4 border-b border-white/10">
            <div className="flex items-center space-x-2">
              <ShoppingBag className="w-5 h-5 text-blue-400" />
              <h2 className="text-xl font-bold tracking-wide text-white">Your Cart</h2>
              <span className="px-2.5 py-0.5 rounded-full bg-blue-500/20 text-blue-300 text-xs font-bold">
                {totalItems} items
              </span>
            </div>
            <button 
              onClick={() => setIsCartOpen(false)} 
              className="p-2 rounded-full glass-pill text-slate-400 hover:text-white cursor-pointer"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Cart Item List */}
          <div className="flex-1 overflow-y-auto py-4 space-y-4 no-scrollbar" data-lenis-prevent="true">
            {cartItems.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center p-6 space-y-4">
                <div className="w-16 h-16 rounded-full bg-white/5 flex items-center justify-center text-slate-500">
                  <ShoppingBag className="w-8 h-8 text-slate-400" />
                </div>
                <p className="text-slate-400 text-sm font-medium">Your shopping cart is empty.</p>
                <button
                  onClick={() => setIsCartOpen(false)}
                  className="glass-pill px-6 py-2.5 rounded-full text-xs font-bold text-blue-400 hover:text-white cursor-pointer"
                >
                  Start Shopping
                </button>
              </div>
            ) : (
              cartItems.map((item) => (
                <div key={item.id} className="glass-card p-3 rounded-2xl flex items-center space-x-3 border border-white/5">
                  <img
                    src={item.product.image_url}
                    alt={item.product.name}
                    className="w-16 h-16 object-contain rounded-xl bg-white/5 p-1"
                  />
                  <div className="flex-1 min-w-0">
                    <h4 className="text-sm font-bold text-white truncate">
                      {item.product.name}
                    </h4>
                    <span className="text-xs text-blue-400 font-bold">
                      ${parseFloat(item.product.price).toFixed(2)}
                    </span>

                    {/* Quantity Modifier */}
                    <div className="flex items-center space-x-2 mt-2">
                      <div className="flex items-center glass-pill rounded-lg px-2 py-0.5 text-xs">
                        <button
                          onClick={() => updateQuantity(item.product.id, item.quantity - 1)}
                          className="text-slate-400 hover:text-white px-1 font-bold cursor-pointer"
                        >
                          -
                        </button>
                        <span className="px-2 font-bold text-white">{item.quantity}</span>
                        <button
                          onClick={() => updateQuantity(item.product.id, item.quantity + 1)}
                          className="text-slate-400 hover:text-white px-1 font-bold cursor-pointer"
                        >
                          +
                        </button>
                      </div>
                      <button
                        onClick={() => removeFromCart(item.product.id)}
                        className="text-slate-500 hover:text-red-400 p-1 cursor-pointer transition-colors"
                        title="Remove"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>

          {/* Footer Summary & Checkout */}
          {cartItems.length > 0 && (
            <div className="pt-4 border-t border-white/10 space-y-4">
              <div className="space-y-1.5 text-sm">
                <div className="flex justify-between text-slate-400">
                  <span>Subtotal</span>
                  <span className="text-slate-200">${subtotal.toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-slate-400">
                  <span>Express Shipping</span>
                  <span className="text-emerald-400 font-bold">FREE</span>
                </div>
                <div className="flex justify-between text-base font-extrabold text-white pt-2 border-t border-white/5">
                  <span>Total</span>
                  <span className="text-blue-400">${subtotal.toFixed(2)}</span>
                </div>
              </div>

              <button
                onClick={() => {
                  setIsCartOpen(false);
                  if (!user) {
                    navigate('/login?redirect=/checkout');
                  } else {
                    navigate('/checkout');
                  }
                }}
                className="btn-glow w-full py-4 rounded-full font-bold text-sm text-white flex items-center justify-center space-x-2 cursor-pointer shadow-xl"
              >
                <span>Proceed to Checkout</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          )}

        </div>
      </div>
    </div>
  );
};

export default CartDrawer;
