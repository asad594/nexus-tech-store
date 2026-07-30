import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  ShoppingBag, Package, Truck, CheckCircle2, Clock, 
  XCircle, ArrowLeft, RefreshCw, AlertCircle, Eye, ShieldCheck 
} from 'lucide-react';
import API from '../api';
import { useAuth } from '../context/AuthContext';

const statusBadgeStyles = {
  pending: 'bg-amber-500/20 text-amber-300 border-amber-500/40',
  processing: 'bg-blue-500/20 text-blue-300 border-blue-500/40',
  shipped: 'bg-indigo-500/20 text-indigo-300 border-indigo-500/40',
  delivered: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40',
  cancelled: 'bg-red-500/20 text-red-300 border-red-500/40',
};

const statusIcons = {
  pending: Clock,
  processing: RefreshCw,
  shipped: Truck,
  delivered: CheckCircle2,
  cancelled: XCircle,
};

const OrdersPage = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [cancellingId, setCancellingId] = useState(null);

  const fetchOrders = async () => {
    setLoading(true);
    try {
      const res = await API.get('/orders/');
      setOrders(res.data);
    } catch (err) {
      console.error('Failed to fetch orders', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!user) {
      navigate('/login?redirect=/orders');
      return;
    }
    fetchOrders();
  }, [user, navigate]);

  const handleCancelOrder = async (orderId) => {
    if (window.confirm('Are you sure you want to cancel this order? Item stock will be returned.')) {
      setCancellingId(orderId);
      try {
        await API.post(`/orders/${orderId}/cancel/`);
        fetchOrders();
      } catch (err) {
        alert(err.response?.data?.error || 'Failed to cancel order.');
      } finally {
        setCancellingId(null);
      }
    }
  };

  if (loading) {
    return (
      <div className="max-w-5xl mx-auto px-4 py-20 text-center space-y-4">
        <div className="w-10 h-10 border-4 border-blue-400 border-t-transparent rounded-full animate-spin mx-auto" />
        <p className="text-slate-400 text-xs font-semibold">Retrieving Order History...</p>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto px-4 md:px-8 py-10 space-y-8">
      {/* Header & Back Button */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <button
            onClick={() => navigate(-1)}
            className="glass-pill px-4 py-1.5 rounded-full text-xs font-bold text-slate-300 hover:text-white flex items-center space-x-2 cursor-pointer w-fit mb-3"
          >
            <ArrowLeft className="w-4 h-4 text-blue-400" />
            <span>Back</span>
          </button>
          <h1 className="text-3xl font-extrabold text-white tracking-tight flex items-center space-x-3">
            <Package className="w-8 h-8 text-blue-400" />
            <span>My Order History</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Track your express dispatch orders, status progress, and item manifests.
          </p>
        </div>

        <button
          onClick={fetchOrders}
          className="glass-pill px-4 py-2 rounded-full text-xs font-bold text-slate-300 hover:text-white flex items-center space-x-2 cursor-pointer w-fit"
        >
          <RefreshCw className="w-4 h-4 text-blue-400" />
          <span>Refresh Status</span>
        </button>
      </div>

      {orders.length === 0 ? (
        <div className="glass-panel rounded-3xl p-12 text-center border border-white/10 space-y-6">
          <div className="w-20 h-20 rounded-full bg-blue-500/10 text-blue-400 flex items-center justify-center mx-auto border border-blue-500/20">
            <ShoppingBag className="w-10 h-10" />
          </div>
          <div className="space-y-2">
            <h3 className="text-xl font-bold text-white">No Orders Placed Yet</h3>
            <p className="text-xs text-slate-400 max-w-sm mx-auto">
              Explore our next-gen electronics catalog and experience automated quantum express dispatch.
            </p>
          </div>
          <Link
            to="/products"
            className="btn-glow px-8 py-3 rounded-full font-bold text-xs text-white inline-block cursor-pointer shadow-lg"
          >
            Browse Products
          </Link>
        </div>
      ) : (
        <div className="space-y-6">
          {orders.map((order) => {
            const StatusIcon = statusIcons[order.status] || Clock;
            return (
              <div
                key={order.id}
                className="glass-panel rounded-3xl p-6 border border-white/10 space-y-6 hover:border-blue-500/30 transition-all shadow-xl"
              >
                {/* Header Row */}
                <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-white/10 text-xs">
                  <div className="space-y-1">
                    <div className="flex items-center space-x-2">
                      <span className="text-slate-400 font-medium">Order ID:</span>
                      <span className="font-mono text-blue-400 font-bold text-sm">#{order.id}</span>
                    </div>
                    <span className="text-[11px] text-slate-400">
                      Placed on {new Date(order.created_at).toLocaleDateString()} at {new Date(order.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>

                  <div className="flex items-center space-x-3">
                    <span
                      className={`px-3 py-1 rounded-full text-xs font-bold uppercase border flex items-center space-x-1.5 ${
                        statusBadgeStyles[order.status] || statusBadgeStyles.pending
                      }`}
                    >
                      <StatusIcon className="w-3.5 h-3.5" />
                      <span>{order.status}</span>
                    </span>

                    <span className="px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-bold uppercase text-[11px]">
                      {order.payment_status}
                    </span>
                  </div>
                </div>

                {/* Items List */}
                <div className="space-y-3">
                  <h4 className="text-[11px] uppercase tracking-widest text-slate-400 font-bold">
                    Order Items ({order.items.length})
                  </h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {order.items.map((item) => (
                      <div
                        key={item.id}
                        className="bg-white/[0.03] p-3.5 rounded-2xl border border-white/5 flex items-center space-x-3"
                      >
                        {item.product_detail?.image_url ? (
                          <img
                            src={item.product_detail.image_url}
                            alt={item.product_name_snapshot}
                            className="w-12 h-12 rounded-xl object-contain bg-white/[0.04] p-1 border border-white/5"
                          />
                        ) : (
                          <div className="w-12 h-12 rounded-xl bg-blue-500/10 flex items-center justify-center text-blue-400">
                            <Package className="w-6 h-6" />
                          </div>
                        )}
                        <div className="flex-1 min-w-0">
                          <h5 className="text-xs font-bold text-white truncate">
                            {item.product_name_snapshot || item.product_detail?.name}
                          </h5>
                          <span className="text-[11px] text-slate-400">
                            {item.quantity} x ${parseFloat(item.price_at_purchase).toFixed(2)}
                          </span>
                        </div>
                        <span className="text-xs font-bold text-blue-400">
                          ${(parseFloat(item.price_at_purchase) * item.quantity).toFixed(2)}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Tracking & Address Footer */}
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pt-4 border-t border-white/10 text-xs">
                  <div className="space-y-1">
                    <span className="text-slate-400 font-medium block">Shipping Address:</span>
                    <p className="text-slate-200 font-semibold">{order.shipping_address}</p>
                    {order.tracking_number && (
                      <div className="flex items-center space-x-1.5 text-blue-400 font-mono text-[11px] pt-1">
                        <Truck className="w-3.5 h-3.5" />
                        <span>Tracking: {order.tracking_number}</span>
                      </div>
                    )}
                  </div>

                  <div className="flex items-center justify-between md:justify-end space-x-4">
                    <div className="text-right">
                      <span className="text-slate-400 block text-[11px]">Total Paid</span>
                      <span className="text-lg font-extrabold text-white">${parseFloat(order.total_amount).toFixed(2)}</span>
                    </div>

                    {(order.status === 'pending' || order.status === 'processing') && (
                      <button
                        onClick={() => handleCancelOrder(order.id)}
                        disabled={cancellingId === order.id}
                        className="px-4 py-2 rounded-full bg-red-500/20 hover:bg-red-500/30 text-red-300 border border-red-500/40 text-xs font-bold transition-colors cursor-pointer"
                      >
                        {cancellingId === order.id ? 'Cancelling...' : 'Cancel Order'}
                      </button>
                    )}
                  </div>
                </div>

              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default OrdersPage;
