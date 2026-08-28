import React from 'react';

/**
 * Reusable animated skeleton placeholder for products, text cards, and lists.
 */
export function SkeletonLoader({ className = '', count = 1, variant = 'rect' }) {
  const items = Array.from({ length: count });

  const getVariantClasses = () => {
    switch (variant) {
      case 'circle':
        return 'rounded-full';
      case 'card':
        return 'h-72 w-full rounded-2xl';
      case 'text':
        return 'h-4 w-3/4 rounded';
      default:
        return 'rounded-xl';
    }
  };

  return (
    <>
      {items.map((_, idx) => (
        <div
          key={idx}
          className={`relative overflow-hidden bg-white/5 border border-white/5 animate-pulse ${getVariantClasses()} ${className}`}
        >
          <div className="absolute inset-0 -translate-x-full bg-gradient-to-r from-transparent via-white/10 to-transparent animate-[shimmer_2s_infinite]" />
        </div>
      ))}
    </>
  );
}

export default SkeletonLoader;
