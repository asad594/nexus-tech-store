import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { CreditCard, ShieldCheck, CheckCircle2, Truck, Lock, ArrowLeft } from 'lucide-react';
import confetti from 'canvas-confetti';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';
import API from '../api';

const CheckoutPage = () => {
  const navigate = useNavigate();
  const { cartItems, subtotal, clearCart } = useCart();
  const { user } = useAuth();

  React.useEffect(() => {
    if (!user) {
      navigate('/login?redirect=/checkout');
    }
  }, [user, navigate]);

  const [step, setStep] = useState(1); // Step 1: Address, Step 2: Payment, Step 3: Confirmation
  const [address, setAddress] = useState('100 Silicon Valley Way, Suite 400, San Jose, CA 95134');
  const [cardNumber, setCardNumber] = useState('4532 •••• •••• 8892');
  const [cardHolder, setCardHolder] = useState(user?.name || 'ALEX N. NEXUS');
  const [expiry, setExpiry] = useState('08/29');
  const [cvv, setCvv] = useState('942');
  const [loading, setLoading] = useState(false);
  const [orderComplete, setOrderComplete] = useState(null);

  const handlePlaceOrder = async (e) => {
    e.preventDefault();
    if (!user) {
      navigate('/login?redirect=checkout');
      return;
    }

    setLoading(true);
    try {
      const response = await API.post('/orders/checkout/', {
        shipping_address: address,
        payment_method: 'Credit Card',
      });

      setOrderComplete(response.data);
      clearCart();

      // Trigger celebratory confetti animation
      confetti({
        particleCount: 120,
        spread: 80,
        origin: { y: 0.6 }
      });
    } catch (err) {
      console.error('Checkout failed', err);
      alert('Order processing failed. Please check connection or try again.');
    } finally {
      setLoading(false);
    }
  };

  if (orderComplete) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-16 text-center space-y-6">
        <div className="glass-panel p-8 md:p-12 rounded-3xl border border-white/10 space-y-6">
          <div className="w-20 h-20 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center mx-auto border border-emerald-500/40 shadow-lg shadow-emerald-500/30 animate-bounce">
            <CheckCircle2 className="w-10 h-10" />
          </div>

          <div className="space-y-2">
            <h1 className="text-3xl font-extrabold text-white tracking-tight">
              Order Confirmed!
            </h1>
            <p className="text-xs text-slate-300">
              Order ID <span className="font-mono text-blue-400">#{orderComplete.id}</span> has been processed for automated express dispatch.
            </p>
          </div>

          <div className="bg-white/[0.03] p-5 rounded-2xl border border-white/5 text-left text-xs space-y-2 max-w-md mx-auto">
            <div className="flex justify-between">
              <span className="text-slate-400">Total Paid:</span>
              <span className="font-bold text-white">${parseFloat(orderComplete.total_amount).toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Shipping Address:</span>
              <span className="font-medium text-slate-200">{orderComplete.shipping_address}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Order Status:</span>
              <span className="font-bold text-blue-400 uppercase">{orderComplete.status}</span>
            </div>
          </div>

          <Link
            to="/products"
            className="btn-glow px-8 py-3.5 rounded-full font-bold text-xs text-white inline-block cursor-pointer shadow-xl"
          >
            Continue Shopping
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto px-4 md:px-8 py-10 space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-full bg-blue-500/10 border border-blue-400/30 flex items-center justify-center text-blue-400">
            <CreditCard className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-2xl md:text-3xl font-extrabold text-white tracking-tight">
              Express Glass Checkout
            </h1>
            <p className="text-xs text-slate-400">
              Guided 3-step end-to-end encrypted checkout
            </p>
          </div>
        </div>

        <Link
          to="/cart"
          className="glass-pill px-4 py-2 rounded-full text-xs font-bold text-slate-300 hover:text-white flex items-center space-x-1.5"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to Cart</span>
        </Link>
      </div>

      {/* Checkout Form & Steps */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        {/* Left Interactive Credit Card & Inputs */}
        <div className="lg:col-span-8 space-y-6">
          <form onSubmit={handlePlaceOrder} className="glass-panel p-6 md:p-8 rounded-3xl border border-white/10 space-y-6">
            
            {/* Step 1: Shipping Address */}
            <div className="space-y-3">
              <h3 className="text-sm font-bold text-blue-400 uppercase tracking-wider flex items-center space-x-2">
                <Truck className="w-4 h-4" />
                <span>1. Shipping Address</span>
              </h3>
              <textarea
                rows={2}
                value={address}
                onChange={(e) => setAddress(e.target.value)}
                required
                className="w-full px-4 py-3 rounded-2xl bg-white/[0.04] border border-white/10 text-white text-xs focus:border-blue-400 focus:outline-none"
              />
            </div>

            {/* Step 2: Payment Mock */}
            <div className="space-y-4 pt-4 border-t border-white/10">
              <h3 className="text-sm font-bold text-blue-400 uppercase tracking-wider flex items-center space-x-2">
                <CreditCard className="w-4 h-4" />
                <span>2. Payment Details</span>
              </h3>

              {/* 3D Chip Card Visualization */}
              <div className="w-full max-w-md h-48 rounded-2xl p-5 bg-gradient-to-tr from-blue-950 via-slate-900 to-indigo-950 border border-white/20 shadow-2xl relative overflow-hidden flex flex-col justify-between mx-auto">
                <div className="absolute top-0 right-0 w-32 h-32 bg-blue-400/20 blur-2xl rounded-full pointer-events-none" />
                <div className="flex justify-between items-center">
                  <div className="w-10 h-7 rounded bg-amber-400/80 border border-amber-300/40 flex items-center justify-center">
                    <div className="w-6 h-4 border border-amber-900/30 rounded-xs" />
                  </div>
                  <span className="text-xs font-bold tracking-widest text-blue-300">NEXUS CARD</span>
                </div>
                <div className="font-mono text-lg font-bold tracking-wider text-white">
                  {cardNumber || '•••• •••• •••• ••••'}
                </div>
                <div className="flex justify-between items-end text-xs">
                  <div>
                    <div className="text-[9px] uppercase tracking-widest text-slate-400">Card Holder</div>
                    <div className="font-bold text-slate-200 uppercase">{cardHolder || 'VALUED CUSTOMER'}</div>
                  </div>
                  <div>
                    <div className="text-[9px] uppercase tracking-widest text-slate-400">Expires</div>
                    <div className="font-bold text-slate-200">{expiry || 'MM/YY'}</div>
                  </div>
                </div>
              </div>

              {/* Card Inputs */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
                <div className="space-y-1">
                  <label className="text-xs font-bold text-slate-300">Card Number</label>
                  <input
                    type="text"
                    value={cardNumber}
                    onChange={(e) => setCardNumber(e.target.value)}
                    required
                    className="w-full px-4 py-2.5 rounded-xl bg-white/[0.04] border border-white/10 text-white font-mono text-xs focus:border-blue-400 focus:outline-none"
                  />
                </div>
                <div className="space-y-1">
                  <label className="text-xs font-bold text-slate-300">Card Holder</label>
                  <input
                    type="text"
                    value={cardHolder}
                    onChange={(e) => setCardHolder(e.target.value)}
                    required
                    className="w-full px-4 py-2.5 rounded-xl bg-white/[0.04] border border-white/10 text-white text-xs focus:border-blue-400 focus:outline-none"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-1">
                  <label className="text-xs font-bold text-slate-300">Expiry Date</label>
                  <input
                    type="text"
                    value={expiry}
                    onChange={(e) => setExpiry(e.target.value)}
                    required
                    className="w-full px-4 py-2.5 rounded-xl bg-white/[0.04] border border-white/10 text-white text-center font-mono text-xs focus:border-blue-400 focus:outline-none"
                  />
                </div>
                <div className="space-y-1">
                  <label className="text-xs font-bold text-slate-300">CVV Security Code</label>
                  <input
                    type="password"
                    value={cvv}
                    onChange={(e) => setCvv(e.target.value)}
                    required
                    maxLength={4}
                    className="w-full px-4 py-2.5 rounded-xl bg-white/[0.04] border border-white/10 text-white text-center font-mono text-xs focus:border-blue-400 focus:outline-none"
                  />
                </div>
              </div>
            </div>

            {!user && (
              <div className="p-4 rounded-2xl bg-amber-500/10 border border-amber-500/20 text-amber-300 text-xs flex items-center justify-between">
                <span>Account required to finalize purchase.</span>
                <Link to="/login?redirect=checkout" className="font-bold underline text-white">
                  Sign In Now
                </Link>
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="btn-glow w-full py-4 rounded-full font-bold text-xs text-white flex items-center justify-center space-x-2 cursor-pointer shadow-xl"
            >
              <Lock className="w-4 h-4 text-blue-200" />
              <span>{loading ? 'Processing Order...' : `Complete Order ($${subtotal.toFixed(2)})`}</span>
            </button>

          </form>
        </div>

        {/* Right Order Breakdown */}
        <div className="lg:col-span-4 space-y-4">
          <div className="glass-panel p-6 rounded-2xl border border-white/10 space-y-4">
            <h3 className="text-base font-bold text-white border-b border-white/10 pb-3">
              Summary ({cartItems.reduce((acc, i) => acc + i.quantity, 0)} Items)
            </h3>

            <div className="space-y-3 max-h-60 overflow-y-auto no-scrollbar">
              {cartItems.map((item) => (
                <div key={item.id} className="flex justify-between items-center text-xs">
                  <div className="flex items-center space-x-2 truncate max-w-[180px]">
                    <span className="font-bold text-blue-400">{item.quantity}x</span>
                    <span className="text-slate-200 truncate">{item.product.name}</span>
                  </div>
                  <span className="font-bold text-white">${(parseFloat(item.product.price) * item.quantity).toFixed(2)}</span>
                </div>
              ))}
            </div>

            <div className="pt-3 border-t border-white/10 flex justify-between text-base font-black text-white">
              <span>Total Due</span>
              <span className="text-blue-400">${subtotal.toFixed(2)}</span>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};

export default CheckoutPage;
