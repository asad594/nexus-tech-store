import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import ScrollVideoHero from '../components/ScrollVideoHero';
import ProductCarousel from '../components/ProductCarousel';
import ProductCard from '../components/ProductCard';
import API from '../api';
import { 
  Sparkles, ArrowRight, ShieldCheck, Cpu, Headphones, 
  Laptop, Smartphone, Tablet, Watch, Zap, Award 
} from 'lucide-react';

const categoryIcons = {
  'Laptops': Laptop,
  'Phones': Smartphone,
  'Tablets': Tablet,
  'Audio': Headphones,
  'Accessories': Watch,
};

const HomePage = () => {
  const navigate = useNavigate();
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [prodRes, catRes] = await Promise.all([
          API.get('/products/'),
          API.get('/categories/'),
        ]);
        setProducts(prodRes.data);
        setCategories(catRes.data);
      } catch (err) {
        console.error('Failed to load homepage data', err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const featuredProducts = products.filter(p => p.is_featured);
  const newReleases = products.filter(p => p.is_new);

  return (
    <div className="space-y-12">
      {/* Scroll-Scrubbed Video Hero */}
      <ScrollVideoHero
        onExploreClick={() => navigate('/products')}
        featuredProduct={products[0]}
      />

      {/* Category Cards Showcase Grid */}
      <section className="max-w-7xl mx-auto px-4 md:px-8 py-8">
        <div className="text-center space-y-2 mb-8">
          <div className="inline-flex items-center space-x-2 px-4 py-1.5 rounded-full glass-pill text-blue-400 text-sm font-bold uppercase tracking-widest border border-blue-400/20">
            <Sparkles className="w-4 h-4" />
            <span>CATEGORIES OF THE FUTURE</span>
          </div>
          <h2 className="text-3xl md:text-4xl font-black text-white tracking-tight">
            Explore Quantum Hardware
          </h2>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-5">
          {categories.map((cat) => {
            const IconComp = categoryIcons[cat.name] || Cpu;
            return (
              <div
                key={cat.id}
                onClick={() => navigate(`/products?category=${cat.name}`)}
                className="glass-card p-6 rounded-2xl flex flex-col items-center justify-center space-y-3 cursor-pointer group hover:border-blue-400/50 shadow-xl"
              >
                <div className="w-14 h-14 rounded-2xl bg-blue-500/10 border border-blue-400/20 flex items-center justify-center text-blue-400 group-hover:scale-110 group-hover:bg-blue-500/20 transition-all">
                  <IconComp className="w-7 h-7" />
                </div>
                <span className="font-bold text-base text-slate-200 group-hover:text-white">
                  {cat.name}
                </span>
                <span className="text-xs text-slate-400 font-medium">
                  {cat.product_count || 3}+ Models
                </span>
              </div>
            );
          })}
        </div>
      </section>

      {/* Featured Collections Carousel */}
      {featuredProducts.length > 0 && (
        <ProductCarousel
          title="Featured Releases 2026"
          subtitle="Handpicked Flagship Tech"
          products={featuredProducts}
          onSelectProduct={(p) => navigate(`/products/${p.id}`)}
        />
      )}

      {/* New Releases Section */}
      <section className="max-w-7xl mx-auto px-4 md:px-8 py-10">
        <div className="glass-panel rounded-3xl p-6 md:p-10 border border-white/10 shadow-2xl">
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between pb-6 border-b border-white/10 mb-8 gap-4">
            <div>
              <div className="flex items-center space-x-2 text-sm font-bold text-blue-400 uppercase tracking-widest mb-1.5">
                <Zap className="w-4 h-4 text-blue-400" />
                <span>FRESH OFF THE PRODUCTION LINE</span>
              </div>
              <h2 className="text-3xl md:text-4xl font-black text-white tracking-tight">
                New Quantum Arrivals
              </h2>
            </div>
            <Link
              to="/products"
              className="glass-pill px-5 py-2.5 rounded-full text-sm font-bold text-slate-200 hover:text-white flex items-center space-x-2 cursor-pointer shadow-md"
            >
              <span>View Full Catalog</span>
              <ArrowRight className="w-4 h-4 text-blue-400" />
            </Link>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {newReleases.slice(0, 8).map((product) => (
              <ProductCard
                key={product.id}
                product={product}
                onSelect={(p) => navigate(`/products/${p.id}`)}
              />
            ))}
          </div>
        </div>
      </section>

      {/* Brand Features Banner */}
      <section className="max-w-7xl mx-auto px-4 md:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="glass-panel p-6 rounded-2xl flex items-center space-x-4 border border-white/10 shadow-lg">
            <div className="w-12 h-12 rounded-xl bg-blue-500/10 border border-blue-400/30 flex items-center justify-center text-blue-400 shrink-0">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <div>
              <h4 className="font-bold text-white text-base">Official Quantum Warranty</h4>
              <p className="text-xs sm:text-sm text-slate-300 mt-0.5">2-Year comprehensive global coverage included.</p>
            </div>
          </div>

          <div className="glass-panel p-6 rounded-2xl flex items-center space-x-4 border border-white/10 shadow-lg">
            <div className="w-12 h-12 rounded-xl bg-cyan-500/10 border border-cyan-400/30 flex items-center justify-center text-cyan-400 shrink-0">
              <Zap className="w-6 h-6" />
            </div>
            <div>
              <h4 className="font-bold text-white text-base">Same-Day Express Dispatch</h4>
              <p className="text-xs sm:text-sm text-slate-300 mt-0.5">Direct fulfillment from our automated glass hubs.</p>
            </div>
          </div>

          <div className="glass-panel p-6 rounded-2xl flex items-center space-x-4 border border-white/10 shadow-lg">
            <div className="w-12 h-12 rounded-xl bg-indigo-500/10 border border-indigo-400/30 flex items-center justify-center text-indigo-400 shrink-0">
              <Award className="w-6 h-6" />
            </div>
            <div>
              <h4 className="font-bold text-white text-base">Authentic Hardware Guarantee</h4>
              <p className="text-xs sm:text-sm text-slate-300 mt-0.5">100% verified original component manufacturing.</p>
            </div>
          </div>
        </div>
      </section>

    </div>
  );
};

export default HomePage;
