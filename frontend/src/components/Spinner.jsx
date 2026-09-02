import React from 'react';

/**
 * Reusable Futuristic Cyber Loading Spinner with glowing gradient pulses.
 *
 * @param {'xs' | 'sm' | 'md' | 'lg' | 'xl'} size - Spinner dimension (default: 'md').
 * @param {'cyan' | 'purple' | 'amber' | 'emerald' | 'white'} color - Glow color theme.
 * @param {string} label - Optional accessibility loading label text.
 * @param {string} className - Optional container styling classes.
 */
export function Spinner({
  size = 'md',
  color = 'cyan',
  label = 'Loading...',
  className = '',
}) {
  const sizeClasses = {
    xs: 'w-3.5 h-3.5 border-2',
    sm: 'w-5 h-5 border-2',
    md: 'w-8 h-8 border-2.5',
    lg: 'w-12 h-12 border-3',
    xl: 'w-16 h-16 border-4',
  };

  const colorClasses = {
    cyan: 'border-cyan-500/20 border-t-cyan-400 drop-shadow-[0_0_10px_rgba(6,182,212,0.6)]',
    purple: 'border-purple-500/20 border-t-purple-400 drop-shadow-[0_0_10px_rgba(168,85,247,0.6)]',
    amber: 'border-amber-500/20 border-t-amber-400 drop-shadow-[0_0_10px_rgba(245,158,11,0.6)]',
    emerald: 'border-emerald-500/20 border-t-emerald-400 drop-shadow-[0_0_10px_rgba(16,185,129,0.6)]',
    white: 'border-white/20 border-t-white drop-shadow-[0_0_8px_rgba(255,255,255,0.5)]',
  };

  return (
    <div
      role="status"
      aria-label={label}
      className={`inline-flex items-center justify-center ${className}`}
    >
      <div
        className={`rounded-full animate-spin ${
          sizeClasses[size] || sizeClasses.md
        } ${colorClasses[color] || colorClasses.cyan}`}
      />
      <span className="sr-only">{label}</span>
    </div>
  );
}

export default Spinner;
