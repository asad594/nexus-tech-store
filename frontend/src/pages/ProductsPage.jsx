import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import ProductCard from '../components/ProductCard';
import API from '../api';
import { 
  Search, ArrowUpDown, Filter, Sparkles, X, 
  Laptop, Smartphone, Tablet, Headphones, Watch, Cpu 
} from 'lucide-react';

const categoryIcons = {
  'All': Sparkles,
  'Laptops': Laptop,
  'Phones': Smartphone,
  'Tablets': Tablet,
  'Audio': Headphones,
  'Accessories': Watch,
};

const ProductsPage = () => {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();

  const initialCat = searchParams.get('category') || 'All';
  const initialSearch = searchParams.get('search') || '';

  const [categories, setCategories] = useState([]);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  // Filters
  const [selectedCategory, setSelectedCategory] = useState(initialCat);
  const [searchQuery, setSearchQuery] = useState(initialSearch);
  const [selectedBrand, setSelectedBrand] = useState('All');
  const [maxPrice, setMaxPrice] = useState(3000);
  const [sortBy, setSortBy] = useState('newest');

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const res = await API.get('/categories/');
        setCategories(res.data);
      } catch (err) {
        console.error('Failed to fetch categories', err);
      }
    };
    fetchCategories();
  }, []);

  useEffect(() => {
    const fetchProducts = async () => {
      setLoading(true);
      try {
        let params = {};
        if (selectedCategory !== 'All') params.category = selectedCategory;
        if (searchQuery) params.search = searchQuery;
        if (selectedBrand !== 'All') params.brand = selectedBrand;
        if (maxPrice < 3000) params.max_price = maxPrice;
        if (sortBy) params.ordering = sortBy;

        const res = await API.get('/products/', { params });
        setProducts(res.data);
      } catch (err) {
        console.error('Failed to fetch products', err);
      } finally {
        setLoading(false);
      }
    };
    fetchProducts();
  }, [selectedCategory, searchQuery, selectedBrand, maxPrice, sortBy]);

  const brands = ['All', ...new Set(products.map(p => p.brand).filter(Boolean))];
  const allCategoryNames = ['All', ...(categories.map(c => c.name))];

  return (
    <div className="max-w-7xl mx-auto px-4 md:px-8 py-10 space-y-8">
      {/* Header Banner */}
      <div className="glass-panel rounded-3xl p-8 border border-white/10 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-80 h-80 bg-blue-500/10 blur-3xl rounded-full pointer-events-none" />
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 relative z-10">
          <div>
            <div className="flex items-center space-x-2 text-sm font-bold text-blue-400 uppercase tracking-widest mb-1.5">
              <Sparkles className="w-4 h-4" />
              <span>NEXUS CATALOG</span>
            </div>
            <h1 className="text-3xl md:text-4xl font-black text-white tracking-tight">
              Electronics Store
            </h1>
            <p className="text-slate-300 text-sm mt-1">
              Filter through quantum processors, OLED displays, and aerospace acoustics.
            </p>
          </div>

          {/* Search Bar */}
          <div className="relative w-full md:w-84">
            <Search className="w-4.5 h-4.5 text-slate-400 absolute left-4 top-3.5" />
            <input
              type="text"
              placeholder="Search laptops, phones, specs..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-11 pr-4 py-3 rounded-full bg-white/[0.04] border border-white/10 text-sm text-white placeholder-slate-400 focus:border-blue-400 focus:outline-none transition-colors"
            />
          </div>
        </div>
      </div>

      {/* Main Container with Sidebar + Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Left Sidebar Filter Panel */}
        <aside className="lg:col-span-3 space-y-6">
          <div className="glass-panel rounded-2xl p-6 border border-white/10 space-y-6 sticky top-24">
            <div className="flex items-center justify-between border-b border-white/10 pb-3">
              <div className="flex items-center space-x-2 text-sm font-bold text-white">
                <Filter className="w-4 h-4 text-blue-400" />
                <span>Filters</span>
              </div>
              <button
                onClick={() => {
                  setSelectedCategory('All');
                  setSearchQuery('');
                  setSelectedBrand('All');
                  setMaxPrice(3000);
                  setSortBy('newest');
                }}
                className="text-[11px] text-blue-400 font-semibold hover:underline cursor-pointer"
              >
                Reset All
              </button>
            </div>

            {/* Category Pills */}
            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-300 uppercase tracking-wider block">
                Category
              </label>
              <div className="space-y-1">
                {allCategoryNames.map((catName) => {
                  const IconComp = categoryIcons[catName] || Cpu;
                  const isActive = selectedCategory === catName;
                  return (
                    <button
                      key={catName}
                      onClick={() => setSelectedCategory(catName)}
                      className={`w-full px-3 py-2 rounded-xl text-xs font-medium flex items-center justify-between transition-colors cursor-pointer ${
                        isActive
                          ? 'bg-blue-500/20 text-blue-300 border border-blue-400/40 font-bold'
                          : 'text-slate-400 hover:text-white hover:bg-white/5'
                      }`}
                    >
                      <div className="flex items-center space-x-2">
                        <IconComp className={`w-3.5 h-3.5 ${isActive ? 'text-blue-400' : 'text-slate-500'}`} />
                        <span>{catName}</span>
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Price Range Slider */}
            <div className="space-y-2 pt-2 border-t border-white/5">
              <div className="flex justify-between text-xs">
                <label className="font-bold text-slate-300 uppercase tracking-wider">Max Price</label>
                <span className="font-bold text-blue-400">${maxPrice}</span>
              </div>
              <input
                type="range"
                min="100"
                max="3000"
                step="100"
                value={maxPrice}
                onChange={(e) => setMaxPrice(Number(e.target.value))}
                className="w-full accent-blue-400 cursor-pointer"
              />
            </div>

            {/* Brand Radio / Pills */}
            <div className="space-y-2 pt-2 border-t border-white/5">
              <label className="text-xs font-bold text-slate-300 uppercase tracking-wider block">
                Brand
              </label>
              <div className="flex flex-wrap gap-1.5">
                {brands.map((b) => (
                  <button
                    key={b}
                    onClick={() => setSelectedBrand(b)}
                    className={`px-3 py-1 rounded-full text-[11px] font-medium transition-colors cursor-pointer ${
                      selectedBrand === b
                        ? 'bg-blue-500/20 text-blue-300 border border-blue-400/40'
                        : 'glass-pill text-slate-400 hover:text-white'
                    }`}
                  >
                    {b}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </aside>

        {/* Right Main Grid */}
        <main className="lg:col-span-9 space-y-6">
          {/* Top Sort & Count Bar */}
          <div className="flex items-center justify-between glass-panel p-4 rounded-2xl border border-white/10 text-xs">
            <span className="text-slate-400">
              Showing <strong className="text-white">{products.length}</strong> products
            </span>

            <div className="flex items-center space-x-2">
              <ArrowUpDown className="w-3.5 h-3.5 text-blue-400" />
              <span className="text-slate-400 hidden sm:inline">Sort by:</span>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="bg-slate-900 border border-white/10 text-xs text-white rounded-lg px-3 py-1.5 font-semibold focus:outline-none cursor-pointer"
              >
                <option value="newest">Newest Arrivals</option>
                <option value="price_low">Price: Low to High</option>
                <option value="price_high">Price: High to Low</option>
                <option value="rating">Top Rated</option>
              </select>
            </div>
          </div>

          {/* Product Grid */}
          {loading ? (
            <div className="py-20 text-center space-y-4">
              <div className="w-10 h-10 border-4 border-blue-400 border-t-transparent rounded-full animate-spin mx-auto" />
              <p className="text-slate-400 text-xs font-semibold">Loading Catalog...</p>
            </div>
          ) : products.length === 0 ? (
            <div className="glass-panel p-12 rounded-3xl text-center space-y-3 border border-white/10">
              <p className="text-slate-400 text-sm font-medium">No products match your selected filter criteria.</p>
              <button
                onClick={() => {
                  setSelectedCategory('All');
                  setSearchQuery('');
                  setSelectedBrand('All');
                  setMaxPrice(3000);
                }}
                className="glass-pill px-6 py-2.5 rounded-full text-xs font-bold text-blue-400 hover:text-white cursor-pointer"
              >
                Reset All Filters
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
              {products.map((product) => (
                <ProductCard
                  key={product.id}
                  product={product}
                  onSelect={(p) => navigate(`/products/${p.id}`)}
                />
              ))}
            </div>
          )}
        </main>

      </div>
    </div>
  );
};

export default ProductsPage;
