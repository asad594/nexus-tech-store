import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ShoppingBag, Trash2, ArrowRight, ShieldCheck, ArrowLeft } from 'lucide-react';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';

const CartPage = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const { cartItems, updateQuantity, removeFromCart, subtotal, totalItems } = useCart();

  return (
    <div className="max-w-5xl mx-auto px-4 md:px-8 py-10 space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-full bg-blue-500/10 border border-blue-400/30 flex items-center justify-center text-blue-400">
            <ShoppingBag className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-2xl md:text-3xl font-extrabold text-white tracking-tight">
              Shopping Cart
            </h1>
            <p className="text-xs text-slate-400">
              Review your quantum hardware selections ({totalItems} items)
            </p>
          </div>
        </div>

        <Link
          to="/products"
          className="glass-pill px-4 py-2 rounded-full text-xs font-bold text-slate-300 hover:text-white flex items-center space-x-1.5"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Continue Shopping</span>
        </Link>
      </div>

      {cartItems.length === 0 ? (
        <div className="glass-panel p-12 rounded-3xl text-center space-y-4 border border-white/10">
          <div className="w-16 h-16 rounded-full bg-white/5 flex items-center justify-center mx-auto text-slate-500">
            <ShoppingBag className="w-8 h-8 text-slate-400" />
          </div>
          <h3 className="text-lg font-bold text-white">Your cart is currently empty</h3>
          <p className="text-xs text-slate-400 max-w-sm mx-auto">
            Explore our futuristic catalog of laptops, phones, tablets, and acoustics.
          </p>
          <Link
            to="/products"
            className="btn-glow px-8 py-3 rounded-full text-xs font-bold text-white inline-block shadow-lg"
          >
            Explore Catalog
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          
          {/* Cart Item List */}
          <div className="lg:col-span-8 space-y-4">
            {cartItems.map((item) => {
              const unitPrice = parseFloat(item.product.price) + (item.variant?.price_delta ? parseFloat(item.variant.price_delta) : 0);
              const thumb = item.variant?.image_url || item.product.image_url;
              return (
                <div
                  key={item.id}
                  className="glass-panel p-4 md:p-5 rounded-2xl flex flex-col sm:flex-row items-center justify-between gap-4 border border-white/10"
                >
                  <div className="flex items-center space-x-4 w-full sm:w-auto">
                    <img
                      src={thumb}
                      alt={item.product.name}
                      className="w-20 h-20 object-contain rounded-xl bg-white/5 p-2 shrink-0"
                    />
                    <div>
                      <h3 className="font-bold text-white text-base">
                        {item.product.name}
                      </h3>
                      {item.variant ? (
                        <div className="flex items-center space-x-2 mt-0.5">
                          <span
                            className="w-3 h-3 rounded-full border border-white/30 shrink-0 inline-block"
                            style={{ backgroundColor: item.variant.hex_code }}
                          />
                          <span className="text-xs text-slate-300 font-semibold">
                            Color: {item.variant.color_name}
                          </span>
                        </div>
                      ) : (
                        <p className="text-xs text-slate-400">
                          Brand: {item.product.brand}
                        </p>
                      )}
                      <span className="text-sm font-extrabold text-blue-400 mt-1 block">
                        ${unitPrice.toFixed(2)}
                      </span>
                    </div>
                  </div>

                  {/* Quantity Modifier & Remove */}
                  <div className="flex items-center space-x-6 w-full sm:w-auto justify-between sm:justify-end border-t sm:border-t-0 pt-3 sm:pt-0 border-white/5">
                    <div className="flex items-center glass-pill rounded-xl px-3 py-1 text-sm">
                      <button
                        onClick={() => updateQuantity(item.id, item.quantity - 1)}
                        className="text-slate-400 hover:text-white px-2 font-bold cursor-pointer"
                      >
                        -
                      </button>
                      <span className="px-3 font-bold text-white">{item.quantity}</span>
                      <button
                        onClick={() => updateQuantity(item.id, item.quantity + 1)}
                        className="text-slate-400 hover:text-white px-2 font-bold cursor-pointer"
                      >
                        +
                      </button>
                    </div>

                    <div className="text-right">
                      <div className="text-sm font-extrabold text-white">
                        ${(unitPrice * item.quantity).toFixed(2)}
                      </div>
                    </div>

                    <button
                      onClick={() => removeFromCart(item.id)}
                      className="text-slate-500 hover:text-red-400 p-2 cursor-pointer transition-colors"
                      title="Remove item"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Right Order Summary */}
          <div className="lg:col-span-4 space-y-4">
            <div className="glass-panel p-6 rounded-2xl border border-white/10 space-y-4">
              <h3 className="text-base font-bold text-white border-b border-white/10 pb-3">
                Order Summary
              </h3>

              <div className="space-y-2 text-xs">
                <div className="flex justify-between text-slate-300">
                  <span>Subtotal ({totalItems} items)</span>
                  <span className="font-bold text-white">${subtotal.toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-slate-300">
                  <span>Express Shipping</span>
                  <span className="font-bold text-emerald-400">FREE</span>
                </div>
                <div className="flex justify-between text-slate-300">
                  <span>Estimated Tax</span>
                  <span className="font-medium text-slate-400">$0.00</span>
                </div>
                <div className="pt-3 border-t border-white/10 flex justify-between text-base font-black text-white">
                  <span>Total Amount</span>
                  <span className="text-blue-400">${subtotal.toFixed(2)}</span>
                </div>
              </div>

              <button
                onClick={() => {
                  if (!user) {
                    navigate('/login?redirect=/checkout');
                  } else {
                    navigate('/checkout');
                  }
                }}
                className="btn-glow w-full py-4 rounded-full font-bold text-xs text-white flex items-center justify-center space-x-2 cursor-pointer shadow-xl"
              >
                <span>Proceed to Checkout</span>
                <ArrowRight className="w-4 h-4" />
              </button>

              <div className="flex items-center justify-center space-x-1.5 text-[11px] text-slate-400 pt-2">
                <ShieldCheck className="w-3.5 h-3.5 text-blue-400" />
                <span>Encrypted Quantum Checkout</span>
              </div>
            </div>
          </div>

        </div>
      )}
    </div>
  );
};

export default CartPage;
