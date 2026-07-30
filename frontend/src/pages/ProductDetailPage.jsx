import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import API from '../api';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';
import ProductCarousel from '../components/ProductCarousel';
import { 
  Star, ShoppingBag, ShieldCheck, Truck, RefreshCw, 
  Cpu, Check, ArrowLeft, MessageSquare, Send, User 
} from 'lucide-react';

const ProductDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { addToCart } = useCart();
  const { user } = useAuth();

  const [product, setProduct] = useState(null);
  const [relatedProducts, setRelatedProducts] = useState([]);
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [quantity, setQuantity] = useState(1);
  const [added, setAdded] = useState(false);

  // Review Form State
  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState('');
  const [submittingReview, setSubmittingReview] = useState(false);
  const [reviewMsg, setReviewMsg] = useState('');

  const fetchDetail = async () => {
    setLoading(true);
    try {
      const res = await API.get(`/products/${id}/`);
      setProduct(res.data);

      // Fetch related products
      const relRes = await API.get(`/products/${id}/related/`);
      setRelatedProducts(relRes.data);

      // Fetch reviews
      const revRes = await API.get(`/products/${id}/reviews/`);
      setReviews(revRes.data);
    } catch (err) {
      console.error('Failed to fetch product details', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDetail();
  }, [id]);

  const handleAddToCart = () => {
    addToCart(product, quantity);
    setAdded(true);
    setTimeout(() => setAdded(false), 2000);
  };

  const handlePostReview = async (e) => {
    e.preventDefault();
    if (!user) {
      navigate('/login?redirect=/products/' + id);
      return;
    }

    setSubmittingReview(true);
    try {
      await API.post(`/products/${id}/reviews/`, {
        rating: parseInt(rating, 10),
        comment,
      });
      setComment('');
      setReviewMsg('Review submitted successfully!');
      fetchDetail();
      setTimeout(() => setReviewMsg(''), 3000);
    } catch (err) {
      console.error('Failed to post review', err);
      alert(err.response?.data?.error || 'Failed to submit review');
    } finally {
      setSubmittingReview(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 md:px-8 py-20 text-center space-y-4">
        <div className="w-10 h-10 border-4 border-blue-400 border-t-transparent rounded-full animate-spin mx-auto" />
        <p className="text-slate-400 text-xs font-semibold">Loading Hardware Specifications...</p>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="max-w-7xl mx-auto px-4 md:px-8 py-20 text-center space-y-4">
        <h2 className="text-2xl font-bold text-white">Product Not Found</h2>
        <Link to="/products" className="btn-glow px-6 py-2.5 rounded-full text-xs font-bold text-white inline-block">
          Return to Products Catalog
        </Link>
      </div>
    );
  }

  const specsList = product.specs ? Object.entries(product.specs) : [];

  return (
    <div className="max-w-7xl mx-auto px-4 md:px-8 py-10 space-y-12">
      {/* Back Button */}
      <button
        onClick={() => navigate(-1)}
        className="glass-pill px-4 py-2 rounded-full text-xs font-bold text-slate-300 hover:text-white flex items-center space-x-2 cursor-pointer w-fit"
      >
        <ArrowLeft className="w-4 h-4 text-blue-400" />
        <span>Back to Products</span>
      </button>

      {/* Main Glass Detail Layout */}
      <div className="glass-panel rounded-3xl p-6 md:p-10 border border-white/10 relative overflow-hidden">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-start">
          
          {/* Left Column: Image Showcase */}
          <div className="lg:col-span-6 flex flex-col items-center">
            <div className="relative w-full h-96 bg-white/[0.02] rounded-2xl p-8 flex items-center justify-center border border-white/5 overflow-hidden">
              <div className="absolute inset-0 bg-blue-500/10 blur-3xl rounded-full" />
              <img
                src={product.image_url}
                alt={product.name}
                className="max-h-80 max-w-full object-contain filter drop-shadow-[0_25px_35px_rgba(0,0,0,0.8)] hover:scale-105 transition-transform duration-500"
              />
            </div>

            {/* Badges */}
            <div className="grid grid-cols-3 gap-3 w-full mt-4 text-center">
              <div className="glass-pill p-3 rounded-xl flex flex-col items-center text-xs text-slate-300">
                <ShieldCheck className="w-5 h-5 text-blue-400 mb-1" />
                <span className="font-semibold">2-Yr Warranty</span>
              </div>
              <div className="glass-pill p-3 rounded-xl flex flex-col items-center text-xs text-slate-300">
                <Truck className="w-5 h-5 text-cyan-400 mb-1" />
                <span className="font-semibold">Free Express</span>
              </div>
              <div className="glass-pill p-3 rounded-xl flex flex-col items-center text-xs text-slate-300">
                <RefreshCw className="w-5 h-5 text-indigo-400 mb-1" />
                <span className="font-semibold">30-Day Return</span>
              </div>
            </div>
          </div>

          {/* Right Column: Specs & Buy Controls */}
          <div className="lg:col-span-6 space-y-6">
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="px-3 py-1 rounded-full bg-blue-500/10 text-blue-400 text-xs font-bold uppercase tracking-wider border border-blue-400/20">
                  {product.category_name} • {product.brand}
                </span>
                <div className="flex items-center space-x-1 text-amber-400 text-sm font-semibold">
                  <Star className="w-4 h-4 fill-amber-400" />
                  <span>{product.rating} ({product.num_reviews || reviews.length} reviews)</span>
                </div>
              </div>

              <h1 className="text-3xl md:text-4xl font-extrabold text-white tracking-tight">
                {product.name}
              </h1>

              <div className="text-3xl font-black text-blue-400 mt-3">
                ${parseFloat(product.price).toFixed(2)}
              </div>
            </div>

            <p className="text-slate-300 text-sm leading-relaxed font-normal">
              {product.description}
            </p>

            {/* Technical Specs Breakdown */}
            {specsList.length > 0 && (
              <div className="space-y-3">
                <h4 className="text-xs uppercase tracking-widest text-slate-400 font-bold flex items-center space-x-1.5">
                  <Cpu className="w-4 h-4 text-blue-400" />
                  <span>Technical Specs Breakdown</span>
                </h4>
                <div className="grid grid-cols-2 gap-3 bg-white/[0.03] p-4 rounded-2xl border border-white/5">
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
              <span className={`w-2.5 h-2.5 rounded-full ${product.stock_qty > 0 ? 'bg-emerald-400 animate-pulse' : 'bg-red-400'}`} />
              <span className="text-slate-300 font-medium">
                {product.stock_qty > 0 ? `In Stock (${product.stock_qty} units available)` : 'Out of Stock'}
              </span>
            </div>

            {/* Quantity Selector & Add to Cart Trigger */}
            <div className="flex items-center space-x-4 pt-4 border-t border-white/10">
              <div className="flex items-center glass-pill rounded-full border-white/10">
                <button
                  onClick={() => setQuantity(Math.max(1, quantity - 1))}
                  className="px-3 py-2.5 text-slate-300 hover:text-white font-bold cursor-pointer"
                >
                  -
                </button>
                <span className="px-4 text-sm font-bold text-white">{quantity}</span>
                <button
                  onClick={() => setQuantity(quantity + 1)}
                  className="px-3 py-2.5 text-slate-300 hover:text-white font-bold cursor-pointer"
                >
                  +
                </button>
              </div>

              <button
                onClick={handleAddToCart}
                disabled={product.stock_qty <= 0}
                className={`flex-1 py-4 px-8 rounded-full font-bold text-sm text-white flex items-center justify-center space-x-2 transition-all cursor-pointer ${
                  added 
                    ? 'bg-emerald-500 shadow-lg shadow-emerald-500/30' 
                    : 'btn-glow'
                }`}
              >
                {added ? (
                  <>
                    <Check className="w-4 h-4 text-white" />
                    <span>Added to Cart!</span>
                  </>
                ) : (
                  <>
                    <ShoppingBag className="w-4 h-4" />
                    <span>Add to Cart (${(parseFloat(product.price) * quantity).toFixed(2)})</span>
                  </>
                )}
              </button>
            </div>
          </div>

        </div>
      </div>

      {/* Customer Reviews Section */}
      <div className="glass-panel rounded-3xl p-6 md:p-10 border border-white/10 space-y-8">
        <div className="flex items-center justify-between border-b border-white/10 pb-4">
          <div className="flex items-center space-x-3">
            <MessageSquare className="w-6 h-6 text-blue-400" />
            <h3 className="text-xl font-bold text-white">Verified Customer Reviews</h3>
          </div>
          <span className="text-xs text-slate-400 font-semibold">
            {reviews.length} Customer Feedback{reviews.length !== 1 ? 's' : ''}
          </span>
        </div>

        {/* Post Review Form */}
        <div className="bg-white/[0.02] p-6 rounded-2xl border border-white/5 space-y-4">
          <h4 className="text-sm font-bold text-white">Write a Review</h4>
          {reviewMsg && (
            <div className="p-3 rounded-xl bg-emerald-500/20 text-emerald-300 text-xs font-semibold border border-emerald-500/40">
              {reviewMsg}
            </div>
          )}

          <form onSubmit={handlePostReview} className="space-y-4">
            <div className="flex items-center space-x-3">
              <span className="text-xs text-slate-300 font-semibold">Rating:</span>
              <div className="flex items-center space-x-1">
                {[1, 2, 3, 4, 5].map((star) => (
                  <Star
                    key={star}
                    onClick={() => setRating(star)}
                    className={`w-5 h-5 cursor-pointer transition-colors ${
                      star <= rating ? 'text-amber-400 fill-amber-400' : 'text-slate-600'
                    }`}
                  />
                ))}
              </div>
            </div>

            <textarea
              rows={3}
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              placeholder={user ? "Write your experience with this futuristic hardware..." : "Sign in to write a review"}
              disabled={!user}
              required
              className="w-full bg-white/[0.03] border border-white/10 rounded-2xl p-4 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-blue-400/50"
            />

            <div className="flex justify-end">
              <button
                type="submit"
                disabled={submittingReview || !user}
                className="btn-glow px-6 py-2.5 rounded-full font-bold text-xs text-white flex items-center space-x-2 cursor-pointer disabled:opacity-50"
              >
                <Send className="w-3.5 h-3.5" />
                <span>{submittingReview ? 'Submitting...' : 'Submit Review'}</span>
              </button>
            </div>
          </form>
        </div>

        {/* Reviews List */}
        {reviews.length === 0 ? (
          <p className="text-xs text-slate-500 text-center py-6">Be the first to review this product!</p>
        ) : (
          <div className="space-y-4">
            {reviews.map((rev) => (
              <div key={rev.id} className="bg-white/[0.02] p-4 rounded-2xl border border-white/5 space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <div className="w-7 h-7 rounded-full bg-blue-500/20 text-blue-400 flex items-center justify-center font-bold text-xs border border-blue-500/30">
                      {rev.user_name ? rev.user_name[0].toUpperCase() : <User className="w-4 h-4" />}
                    </div>
                    <span className="text-xs font-bold text-slate-200">{rev.user_name}</span>
                  </div>

                  <div className="flex items-center space-x-1 text-amber-400 text-xs">
                    {[...Array(rev.rating)].map((_, i) => (
                      <Star key={i} className="w-3.5 h-3.5 fill-amber-400" />
                    ))}
                  </div>
                </div>

                <p className="text-xs text-slate-300 pl-9 font-normal">{rev.comment}</p>
                <span className="text-[10px] text-slate-500 pl-9 block">
                  {new Date(rev.created_at).toLocaleDateString()}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Related Products Carousel */}
      {relatedProducts.length > 0 && (
        <ProductCarousel
          title="Related Electronics"
          subtitle="More from this category"
          products={relatedProducts}
          onSelectProduct={(p) => navigate(`/products/${p.id}`)}
        />
      )}
    </div>
  );
};

export default ProductDetailPage;
