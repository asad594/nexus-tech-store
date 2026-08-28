import React, { useState, useEffect } from 'react';
import { ArrowUp } from 'lucide-react';

/**
 * Floating glassmorphism scroll-to-top button with smooth transition.
 */
export function BackToTop({ showThreshold = 400 }) {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const checkScroll = () => {
      if (window.scrollY > showThreshold) {
        setIsVisible(true);
      } else {
        setIsVisible(false);
      }
    };

    window.addEventListener('scroll', checkScroll, { passive: true });
    return () => window.removeEventListener('scroll', checkScroll);
  }, [showThreshold]);

  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth',
    });
  };

  if (!isVisible) return null;

  return (
    <button
      onClick={scrollToTop}
      aria-label="Back to Top"
      className="fixed bottom-6 right-6 z-40 p-3 rounded-full bg-[#12121e]/80 border border-cyan-500/30 text-cyan-400 backdrop-blur-xl shadow-[0_0_20px_rgba(0,240,255,0.2)] hover:bg-cyan-500/20 hover:scale-110 active:scale-95 transition-all duration-300 group"
    >
      <ArrowUp className="w-5 h-5 group-hover:-translate-y-0.5 transition-transform" />
    </button>
  );
}

export default BackToTop;
