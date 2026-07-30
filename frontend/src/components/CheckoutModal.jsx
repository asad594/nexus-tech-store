import React, { useState } from 'react';
import { X, CreditCard, ShieldCheck, CheckCircle2, Truck, Lock } from 'lucide-react';
import confetti from 'canvas-confetti';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';
import API from '../api';

const CheckoutModal = ({ isOpen, onClose, onOpenAuth }) => {
  const { cartItems, subtotal, clearCart } = useCart();
  const { user } = useAuth();

  const [address, setAddress] = useState('100 Silicon Valley Way, Suite 400, San Jose, CA 95134');
  const [cardNumber, setCardNumber] = useState('4532 •••• •••• 8892');
  const [cardHolder, setCardHolder] = useState(user?.name || 'ALEX N. NEXUS');
  const [expiry, setExpiry] = useState('08/29');
  const [cvv, setCvv] = useState('942');
  const [loading, setLoading] = useState(false);
  const [orderComplete, setOrderComplete] = useState(null);

  if (!isOpen) return null;

  const handlePlaceOrder = async (e) => {
    e.preventDefault();
    if (!user) {
      onOpenAuth();
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
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 }
      });
    } catch (err) {
      console.error('Checkout failed', err);
      alert('Order processing failed. Please check connection or try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-fade-in overflow-y-auto">
      <div className="relative w-full max-w-3xl glass-panel rounded-3xl p-6 md:p-8 my-8 shadow-2xl border border-white/10 text-slate-100 max-h-[90vh] overflow-y-auto no-scrollbar">
        
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-6 right-6 p-2 rounded-full glass-pill text-slate-400 hover:text-white cursor-pointer transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        {orderComplete ? (
          /* Order Confirmation Screen */
          <div className="py-8 text-center space-y-6">
            <div className="w-20 h-20 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center mx-auto border border-emerald-500/40 shadow-lg shadow-emerald-500/30 animate-bounce">
              <CheckCircle2 className="w-10 h-10" />
            </div>
            
            <div className="space-y-2">
              <h2 className="text-3xl font-extrabold text-white tracking-tight">
                Order Confirmed!
              </h2>
              <p className="text-sm text-slate-300">
                Order ID <span className="font-mono text-blue-400">#{orderComplete.id}</span> has been dispatched for instant express delivery.
              </p>
            </div>

            <div className="bg-white/[0.03] p-4 rounded-2xl border border-white/5 max-w-md mx-auto text-left text-xs space-y-2">
              <div className="flex justify-between">
                <span className="text-slate-400">Total Paid:</span>
                <span className="font-bold text-white">${parseFloat(orderComplete.total_amount).toFixed(2)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Shipping Address:</span>
                <span className="font-medium text-slate-200">{orderComplete.shipping_address}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Status:</span>
                <span className="font-bold text-blue-400 uppercase">{orderComplete.status}</span>
              </div>
            </div>

            <button
              onClick={onClose}
              className="btn-glow px-8 py-3.5 rounded-full font-bold text-sm text-white cursor-pointer"
            >
              Continue Shopping
            </button>
          </div>
        ) : (
          /* Checkout Form */
          <form onSubmit={handlePlaceOrder} className="space-y-6">
            <div>
              <h2 className="text-2xl font-black text-white tracking-wide flex items-center space-x-2">
                <CreditCard className="w-6 h-6 text-blue-400" />
                <span>Express Glass Checkout</span>
              </h2>
              <p className="text-xs text-slate-400 mt-1">
                Encrypted end-to-end transaction secured by NEXUS Quantum Shield.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-12 gap-8">
              {/* Left Column: Interactive Futuristic Credit Card Preview */}
              <div className="md:col-span-5 space-y-4">
                <div className="w-full h-48 rounded-2xl p-5 bg-gradient-to-tr from-blue-900/80 via-slate-900 to-indigo-900/80 border border-white/20 shadow-xl relative overflow-hidden flex flex-col justify-between">
                  <div className="absolute top-0 right-0 w-32 h-32 bg-blue-400/20 blur-2xl rounded-full pointer-events-none" />
                  
                  {/* Card Chip */}
                  <div className="flex justify-between items-center">
                    <div className="w-10 h-7 rounded bg-amber-400/80 border border-amber-300/40 flex items-center justify-center">
                      <div className="w-6 h-4 border border-amber-900/30 rounded-xs" />
                    </div>
                    <span className="text-xs font-bold tracking-widest text-blue-300">NEXUS CARD</span>
                  </div>

                  {/* Card Number */}
                  <div className="font-mono text-lg font-bold tracking-wider text-white">
                    {cardNumber || '•••• •••• •••• ••••'}
                  </div>

                  {/* Card Bottom Info */}
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

                {/* Order Summary Box */}
                <div className="bg-white/[0.03] p-4 rounded-2xl border border-white/5 space-y-2 text-xs">
                  <div className="font-bold text-slate-200 uppercase tracking-wider mb-1">
                    Order Summary ({cartItems.reduce((acc, i) => acc + i.quantity, 0)} Items)
                  </div>
                  {cartItems.map((item) => (
                    <div key={item.id} className="flex justify-between text-slate-300">
                      <span className="truncate max-w-[180px]">{item.quantity}x {item.product.name}</span>
                      <span className="font-bold">${(parseFloat(item.product.price) * item.quantity).toFixed(2)}</span>
                    </div>
                  ))}
                  <div className="pt-2 border-t border-white/10 flex justify-between font-extrabold text-sm text-white">
                    <span>Total Amount</span>
                    <span className="text-blue-400">${subtotal.toFixed(2)}</span>
                  </div>
                </div>
              </div>

              {/* Right Column: Inputs */}
              <div className="md:col-span-7 space-y-4">
                {/* Shipping Address */}
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-slate-300 uppercase tracking-wider">
                    Shipping Address
                  </label>
                  <textarea
                    rows={2}
                    value={address}
                    onChange={(e) => setAddress(e.target.value)}
                    required
                    className="w-full px-4 py-2.5 rounded-xl bg-white/[0.04] border border-white/10 text-white text-xs focus:border-blue-400 focus:outline-none transition-colors"
                  />
                </div>

                {/* Card Details */}
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-slate-300 uppercase tracking-wider">
                    Card Number
                  </label>
                  <input
                    type="text"
                    value={cardNumber}
                    onChange={(e) => setCardNumber(e.target.value)}
                    required
                    className="w-full px-4 py-2.5 rounded-xl bg-white/[0.04] border border-white/10 text-white text-xs font-mono focus:border-blue-400 focus:outline-none transition-colors"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-1.5">
                    <label className="text-xs font-bold text-slate-300 uppercase tracking-wider">
                      Card Holder
                    </label>
                    <input
                      type="text"
                      value={cardHolder}
                      onChange={(e) => setCardHolder(e.target.value)}
                      required
                      className="w-full px-4 py-2.5 rounded-xl bg-white/[0.04] border border-white/10 text-white text-xs focus:border-blue-400 focus:outline-none transition-colors"
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-2">
                    <div className="space-y-1.5">
                      <label className="text-xs font-bold text-slate-300 uppercase tracking-wider">
                        Expiry
                      </label>
                      <input
                        type="text"
                        value={expiry}
                        onChange={(e) => setExpiry(e.target.value)}
                        required
                        className="w-full px-3 py-2.5 rounded-xl bg-white/[0.04] border border-white/10 text-white text-xs text-center font-mono focus:border-blue-400 focus:outline-none transition-colors"
                      />
                    </div>
                    <div className="space-y-1.5">
                      <label className="text-xs font-bold text-slate-300 uppercase tracking-wider">
                        CVV
                      </label>
                      <input
                        type="password"
                        value={cvv}
                        onChange={(e) => setCvv(e.target.value)}
                        required
                        maxLength={4}
                        className="w-full px-3 py-2.5 rounded-xl bg-white/[0.04] border border-white/10 text-white text-xs text-center font-mono focus:border-blue-400 focus:outline-none transition-colors"
                      />
                    </div>
                  </div>
                </div>

                {/* Authentication Note */}
                {!user && (
                  <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-300 text-xs flex items-center justify-between">
                    <span>Account required to complete order.</span>
                    <button
                      type="button"
                      onClick={onOpenAuth}
                      className="font-bold underline cursor-pointer hover:text-white"
                    >
                      Login Now
                    </button>
                  </div>
                )}

                {/* Submit Action */}
                <button
                  type="submit"
                  disabled={loading}
                  className="btn-glow w-full py-4 rounded-full font-bold text-sm text-white flex items-center justify-center space-x-2 cursor-pointer shadow-xl mt-4"
                >
                  <Lock className="w-4 h-4 text-blue-200" />
                  <span>{loading ? 'Processing Payment...' : `Complete Order ($${subtotal.toFixed(2)})`}</span>
                </button>
              </div>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};

export default CheckoutModal;
