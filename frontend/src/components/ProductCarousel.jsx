import React, { useRef, useState } from 'react';
import { ChevronLeft, ChevronRight, Sparkles } from 'lucide-react';
import ProductCard from './ProductCard';

const ProductCarousel = ({ title, subtitle, products, onSelectProduct }) => {
  const scrollRef = useRef(null);
  const [activeIndex, setActiveIndex] = useState(0);

  const scroll = (direction) => {
    if (scrollRef.current) {
      const { scrollLeft, clientWidth } = scrollRef.current;
      const scrollAmount = clientWidth * 0.75;
      const newScrollLeft = direction === 'left' 
        ? scrollLeft - scrollAmount 
        : scrollLeft + scrollAmount;

      scrollRef.current.scrollTo({
        left: newScrollLeft,
        behavior: 'smooth'
      });
    }
  };

  const handleScroll = () => {
    if (scrollRef.current) {
      const { scrollLeft, clientWidth } = scrollRef.current;
      const index = Math.round(scrollLeft / (clientWidth * 0.3));
      setActiveIndex(Math.min(index, products.length - 1));
    }
  };

  return (
    <section className="py-10 px-4 md:px-8 max-w-7xl mx-auto">
      {/* Header with Title and Navigation Controls */}
      <div className="flex flex-col md:flex-row md:items-end justify-between mb-6 space-y-4 md:space-y-0">
        <div>
          <div className="flex items-center space-x-2 text-sm font-bold text-blue-400 uppercase tracking-widest mb-1.5">
            <Sparkles className="w-4 h-4" />
            <span>{subtitle || 'Handpicked Innovation'}</span>
          </div>
          <h2 className="text-3xl md:text-4xl font-black text-white tracking-tight">
            {title || 'Featured Releases'}
          </h2>
        </div>

        {/* Arrow Controls */}
        <div className="flex items-center space-x-2">
          <button
            onClick={() => scroll('left')}
            className="glass-pill p-2.5 rounded-full text-slate-300 hover:text-white hover:border-blue-400/50 cursor-pointer"
            aria-label="Previous Products"
          >
            <ChevronLeft className="w-5 h-5" />
          </button>
          <button
            onClick={() => scroll('right')}
            className="glass-pill p-2.5 rounded-full text-slate-300 hover:text-white hover:border-blue-400/50 cursor-pointer"
            aria-label="Next Products"
          >
            <ChevronRight className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Horizontal Carousel Track */}
      <div
        ref={scrollRef}
        onScroll={handleScroll}
        data-lenis-prevent="true"
        className="flex space-x-6 overflow-x-auto no-scrollbar py-4 px-1 scroll-smooth"
      >
        {products.map((product) => (
          <div key={product.id} className="min-w-[280px] sm:min-w-[320px] max-w-[340px] shrink-0">
            <ProductCard product={product} onSelect={onSelectProduct} />
          </div>
        ))}
      </div>

      {/* Pagination Dots */}
      <div className="flex justify-center items-center space-x-2 mt-6">
        {products.slice(0, Math.min(6, products.length)).map((_, idx) => (
          <button
            key={idx}
            onClick={() => {
              if (scrollRef.current) {
                scrollRef.current.scrollTo({
                  left: idx * 300,
                  behavior: 'smooth'
                });
              }
            }}
            className={`h-1.5 rounded-full transition-all duration-300 ${
              activeIndex === idx
                ? 'w-8 bg-blue-400 shadow-[0_0_10px_#4da6ff]'
                : 'w-2 bg-white/20 hover:bg-white/40'
            }`}
          />
        ))}
      </div>
    </section>
  );
};

export default ProductCarousel;
