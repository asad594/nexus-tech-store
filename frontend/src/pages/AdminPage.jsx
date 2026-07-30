import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Shield, Package, ShoppingBag, DollarSign, AlertTriangle, 
  Plus, Edit3, Trash2, X, RefreshCw 
} from 'lucide-react';
import API from '../api';
import { useAuth } from '../context/AuthContext';

const AdminPage = () => {
  const navigate = useNavigate();
  const { user } = useAuth();

  const [activeTab, setActiveTab] = useState('products');
  const [products, setProducts] = useState([]);
  const [orders, setOrders] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);

  // Form State
  const [editingProduct, setEditingProduct] = useState(null);
  const [showProductModal, setShowProductModal] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    category: 1,
    price: '',
    brand: 'NEXUS',
    description: '',
    specs: '{"chip": "Quantum M3", "ram": "16GB"}',
    stock_qty: 20,
    image_url: 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?q=80&w=1000',
    is_featured: false,
    is_new: true,
  });

  const fetchData = async () => {
    setLoading(true);
    try {
      const [prodRes, orderRes, catRes] = await Promise.all([
        API.get('/products/'),
        API.get('/orders/'),
        API.get('/categories/'),
      ]);
      setProducts(prodRes.data);
      setOrders(orderRes.data);
      setCategories(catRes.data);
    } catch (err) {
      console.error('Failed to fetch admin data', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!user) {
      navigate('/login?redirect=/admin');
      return;
    }
    if (user.role !== 'admin') {
      alert('Access Denied: Store Admin privileges required.');
      navigate('/');
      return;
    }
    fetchData();
  }, [user, navigate]);

  const totalRevenue = orders.reduce((sum, o) => sum + parseFloat(o.total_amount || 0), 0);
  const lowStockCount = products.filter(p => p.stock_qty <= 10).length;

  const handleSaveProduct = async (e) => {
    e.preventDefault();
    try {
      let parsedSpecs = {};
      try {
        parsedSpecs = JSON.parse(formData.specs);
      } catch (jsonErr) {
        alert('Invalid Specs JSON format. Please pass valid JSON.');
        return;
      }

      const payload = {
        ...formData,
        price: parseFloat(formData.price),
        stock_qty: parseInt(formData.stock_qty, 10),
        specs: parsedSpecs,
      };

      if (editingProduct) {
        await API.put(`/products/${editingProduct.id}/`, payload);
      } else {
        await API.post('/products/', payload);
      }

      setShowProductModal(false);
      setEditingProduct(null);
      fetchData();
    } catch (err) {
      console.error('Error saving product', err);
      alert('Failed to save product. Ensure you have admin permissions.');
    }
  };

  const handleDeleteProduct = async (id) => {
    if (window.confirm('Are you sure you want to delete this product?')) {
      try {
        await API.delete(`/products/${id}/`);
        fetchData();
      } catch (err) {
        console.error('Error deleting product', err);
      }
    }
  };

  const handleUpdateOrderStatus = async (orderId, newStatus) => {
    try {
      await API.patch(`/orders/${orderId}/update_status/`, { status: newStatus });
      fetchData();
    } catch (err) {
      console.error('Error updating order status', err);
    }
  };

  const openNewProductModal = () => {
    setEditingProduct(null);
    setFormData({
      name: '',
      category: categories[0]?.id || 1,
      price: '1299.00',
      brand: 'NEXUS',
      description: 'Futuristic high-performance electronic device.',
      specs: '{"chip": "Quantum M3", "ram": "16GB", "storage": "512GB"}',
      stock_qty: 25,
      image_url: 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?q=80&w=1000',
      is_featured: true,
      is_new: true,
    });
    setShowProductModal(true);
  };

  const openEditProductModal = (prod) => {
    setEditingProduct(prod);
    setFormData({
      name: prod.name,
      category: prod.category,
      price: prod.price,
      brand: prod.brand,
      description: prod.description,
      specs: JSON.stringify(prod.specs, null, 2),
      stock_qty: prod.stock_qty,
      image_url: prod.image_url,
      is_featured: prod.is_featured,
      is_new: prod.is_new,
    });
    setShowProductModal(true);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 md:px-8 py-10 space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-white/10 pb-6">
        <div className="flex items-center space-x-3">
          <div className="w-12 h-12 rounded-2xl bg-blue-500/20 border border-blue-400/40 flex items-center justify-center text-blue-400">
            <Shield className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl md:text-3xl font-black text-white tracking-tight">
              NEXUS Admin Console
            </h1>
            <p className="text-xs text-blue-400 font-medium">
              Store Analytics & Catalog Management
            </p>
          </div>
        </div>
      </div>

      {/* Metrics Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="glass-panel p-5 rounded-2xl border border-white/10 space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>Total Sales</span>
            <DollarSign className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-black text-white">${totalRevenue.toFixed(2)}</div>
        </div>

        <div className="glass-panel p-5 rounded-2xl border border-white/10 space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>Total Orders</span>
            <ShoppingBag className="w-4 h-4 text-blue-400" />
          </div>
          <div className="text-2xl font-black text-white">{orders.length}</div>
        </div>

        <div className="glass-panel p-5 rounded-2xl border border-white/10 space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>Active Products</span>
            <Package className="w-4 h-4 text-indigo-400" />
          </div>
          <div className="text-2xl font-black text-white">{products.length}</div>
        </div>

        <div className="glass-panel p-5 rounded-2xl border border-white/10 space-y-1">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>Low Stock Alerts</span>
            <AlertTriangle className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl font-black text-amber-300">{lowStockCount}</div>
        </div>
      </div>

      {/* Main Glass Panel */}
      <div className="glass-panel p-6 md:p-8 rounded-3xl border border-white/10 space-y-6">
        
        {/* Tabs Bar */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between pb-4 border-b border-white/10 gap-4">
          <div className="flex space-x-2">
            <button
              onClick={() => setActiveTab('products')}
              className={`px-5 py-2.5 rounded-full text-xs font-bold transition-all cursor-pointer ${
                activeTab === 'products'
                  ? 'bg-gradient-blue text-white shadow-md'
                  : 'glass-pill text-slate-400 hover:text-white'
              }`}
            >
              Manage Products ({products.length})
            </button>
            <button
              onClick={() => setActiveTab('orders')}
              className={`px-5 py-2.5 rounded-full text-xs font-bold transition-all cursor-pointer ${
                activeTab === 'orders'
                  ? 'bg-gradient-blue text-white shadow-md'
                  : 'glass-pill text-slate-400 hover:text-white'
              }`}
            >
              Manage Orders ({orders.length})
            </button>
          </div>

          {activeTab === 'products' && (
            <button
              onClick={openNewProductModal}
              className="btn-glow px-5 py-2.5 rounded-full text-xs font-bold text-white flex items-center space-x-1.5 cursor-pointer shadow-lg"
            >
              <Plus className="w-4 h-4" />
              <span>Add New Product</span>
            </button>
          )}
        </div>

        {/* Products Table */}
        {activeTab === 'products' && (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="text-slate-400 border-b border-white/10 uppercase tracking-wider">
                  <th className="py-3 px-4">Product</th>
                  <th className="py-3 px-4">Category</th>
                  <th className="py-3 px-4">Price</th>
                  <th className="py-3 px-4">Stock</th>
                  <th className="py-3 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {products.map((prod) => (
                  <tr key={prod.id} className="hover:bg-white/[0.02] transition-colors">
                    <td className="py-3 px-4 flex items-center space-x-3">
                      <img src={prod.image_url} alt="" className="w-10 h-10 object-contain rounded-xl bg-white/5 p-1" />
                      <div>
                        <div className="font-bold text-white max-w-[200px] truncate">{prod.name}</div>
                        <div className="text-[10px] text-slate-500">{prod.brand}</div>
                      </div>
                    </td>
                    <td className="py-3 px-4 text-slate-300 font-medium">{prod.category_name}</td>
                    <td className="py-3 px-4 text-blue-400 font-bold">${parseFloat(prod.price).toFixed(2)}</td>
                    <td className="py-3 px-4">
                      <span className={`px-2.5 py-1 rounded-full font-bold text-[10px] ${
                        prod.stock_qty > 10 
                          ? 'bg-emerald-500/20 text-emerald-300' 
                          : 'bg-amber-500/20 text-amber-300'
                      }`}>
                        {prod.stock_qty} in stock
                      </span>
                    </td>
                    <td className="py-3 px-4 text-right space-x-2">
                      <button
                        onClick={() => openEditProductModal(prod)}
                        className="p-1.5 rounded-lg glass-pill text-slate-300 hover:text-white cursor-pointer"
                        title="Edit Product"
                      >
                        <Edit3 className="w-3.5 h-3.5" />
                      </button>
                      <button
                        onClick={() => handleDeleteProduct(prod.id)}
                        className="p-1.5 rounded-lg glass-pill text-slate-300 hover:text-red-400 cursor-pointer"
                        title="Delete Product"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Orders List */}
        {activeTab === 'orders' && (
          <div className="space-y-4">
            {orders.length === 0 ? (
              <p className="text-center py-12 text-slate-400 text-xs">No orders recorded yet.</p>
            ) : (
              orders.map((ord) => (
                <div key={ord.id} className="glass-card p-4 rounded-2xl border border-white/5 space-y-3">
                  <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center text-xs border-b border-white/5 pb-2 gap-2">
                    <div>
                      <span className="font-mono font-bold text-blue-400">Order #{ord.id}</span>
                      <span className="text-slate-400 ml-2">by {ord.user_name} ({ord.user_email})</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className="text-slate-400">Status:</span>
                      <select
                        value={ord.status}
                        onChange={(e) => handleUpdateOrderStatus(ord.id, e.target.value)}
                        className="bg-slate-900 border border-white/10 text-xs rounded-lg px-2.5 py-1 text-white font-bold uppercase focus:outline-none"
                      >
                        <option value="pending">Pending</option>
                        <option value="processing">Processing</option>
                        <option value="completed">Completed</option>
                        <option value="cancelled">Cancelled</option>
                      </select>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                    {ord.items?.map((item) => (
                      <div key={item.id} className="flex items-center space-x-2 bg-white/[0.02] p-2 rounded-xl">
                        <span className="font-bold text-blue-400">{item.quantity}x</span>
                        <span className="text-slate-200 truncate">{item.product_detail?.name || 'Product'}</span>
                        <span className="ml-auto font-semibold text-slate-400">${item.price_at_purchase}</span>
                      </div>
                    ))}
                  </div>

                  <div className="flex justify-between items-center text-xs pt-1 text-slate-400">
                    <span>Address: {ord.shipping_address}</span>
                    <span className="text-sm font-extrabold text-white">Total: ${parseFloat(ord.total_amount).toFixed(2)}</span>
                  </div>
                </div>
              ))
            )}
          </div>
        )}

      </div>

      {/* Add / Edit Product Modal */}
      {showProductModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md">
          <div className="glass-panel p-6 rounded-3xl max-w-lg w-full space-y-4 border border-white/10 text-xs">
            <div className="flex justify-between items-center">
              <h3 className="text-base font-bold text-white">
                {editingProduct ? 'Edit Electronic Product' : 'Add New Product'}
              </h3>
              <button onClick={() => setShowProductModal(false)} className="text-slate-400 hover:text-white cursor-pointer">
                <X className="w-4 h-4" />
              </button>
            </div>

            <form onSubmit={handleSaveProduct} className="space-y-3">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-slate-300 font-bold block mb-1">Product Name</label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    required
                    className="w-full px-3 py-2 rounded-xl bg-white/[0.04] border border-white/10 text-white focus:outline-none"
                  />
                </div>
                <div>
                  <label className="text-slate-300 font-bold block mb-1">Category</label>
                  <select
                    value={formData.category}
                    onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-white/10 text-white focus:outline-none"
                  >
                    {categories.map((c) => (
                      <option key={c.id} value={c.id}>{c.name}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-3 gap-3">
                <div>
                  <label className="text-slate-300 font-bold block mb-1">Price ($)</label>
                  <input
                    type="number"
                    step="0.01"
                    value={formData.price}
                    onChange={(e) => setFormData({ ...formData, price: e.target.value })}
                    required
                    className="w-full px-3 py-2 rounded-xl bg-white/[0.04] border border-white/10 text-white focus:outline-none"
                  />
                </div>
                <div>
                  <label className="text-slate-300 font-bold block mb-1">Brand</label>
                  <input
                    type="text"
                    value={formData.brand}
                    onChange={(e) => setFormData({ ...formData, brand: e.target.value })}
                    required
                    className="w-full px-3 py-2 rounded-xl bg-white/[0.04] border border-white/10 text-white focus:outline-none"
                  />
                </div>
                <div>
                  <label className="text-slate-300 font-bold block mb-1">Stock Qty</label>
                  <input
                    type="number"
                    value={formData.stock_qty}
                    onChange={(e) => setFormData({ ...formData, stock_qty: e.target.value })}
                    required
                    className="w-full px-3 py-2 rounded-xl bg-white/[0.04] border border-white/10 text-white focus:outline-none"
                  />
                </div>
              </div>

              <div>
                <label className="text-slate-300 font-bold block mb-1">Description</label>
                <textarea
                  rows={2}
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  required
                  className="w-full px-3 py-2 rounded-xl bg-white/[0.04] border border-white/10 text-white focus:outline-none"
                />
              </div>

              <div>
                <label className="text-slate-300 font-bold block mb-1">Specs (JSON string)</label>
                <textarea
                  rows={2}
                  value={formData.specs}
                  onChange={(e) => setFormData({ ...formData, specs: e.target.value })}
                  required
                  className="w-full px-3 py-2 rounded-xl bg-white/[0.04] border border-white/10 text-white font-mono text-[11px] focus:outline-none"
                />
              </div>

              <div>
                <label className="text-slate-300 font-bold block mb-1">Image URL</label>
                <input
                  type="url"
                  value={formData.image_url}
                  onChange={(e) => setFormData({ ...formData, image_url: e.target.value })}
                  required
                  className="w-full px-3 py-2 rounded-xl bg-white/[0.04] border border-white/10 text-white focus:outline-none"
                />
              </div>

              <div className="flex justify-end space-x-2 pt-2">
                <button
                  type="button"
                  onClick={() => setShowProductModal(false)}
                  className="glass-pill px-4 py-2 rounded-full text-slate-400 hover:text-white cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="btn-glow px-6 py-2 rounded-full font-bold text-white cursor-pointer"
                >
                  Save Product
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
};

export default AdminPage;
