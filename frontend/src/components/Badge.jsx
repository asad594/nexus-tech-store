import React from 'react';

/**
 * Reusable Badge & Status Pill component with neon cyberpunk glowing styles.
 */
export function Badge({
  children,
  variant = 'cyan',
  size = 'md',
  dot = false,
  className = '',
}) {
  const variantStyles = {
    cyan: 'bg-cyan-500/10 text-cyan-400 border-cyan-500/30 shadow-[0_0_10px_rgba(6,182,212,0.15)]',
    purple: 'bg-purple-500/10 text-purple-400 border-purple-500/30 shadow-[0_0_10px_rgba(168,85,247,0.15)]',
    emerald: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30 shadow-[0_0_10px_rgba(16,185,129,0.15)]',
    amber: 'bg-amber-500/10 text-amber-400 border-amber-500/30 shadow-[0_0_10px_rgba(245,158,11,0.15)]',
    rose: 'bg-rose-500/10 text-rose-400 border-rose-500/30 shadow-[0_0_10px_rgba(244,63,94,0.15)]',
    neutral: 'bg-white/5 text-gray-300 border-white/10',
  };

  const sizeStyles = {
    sm: 'text-xs px-2 py-0.5',
    md: 'text-xs px-2.5 py-1',
    lg: 'text-sm px-3.5 py-1.5',
  };

  const dotColors = {
    cyan: 'bg-cyan-400 shadow-[0_0_6px_#22d3ee]',
    purple: 'bg-purple-400 shadow-[0_0_6px_#c084fc]',
    emerald: 'bg-emerald-400 shadow-[0_0_6px_#34d399]',
    amber: 'bg-amber-400 shadow-[0_0_6px_#fbbf24]',
    rose: 'bg-rose-400 shadow-[0_0_6px_#fb7185]',
    neutral: 'bg-gray-400',
  };

  return (
    <span
      className={`inline-flex items-center gap-1.5 font-medium rounded-full border backdrop-blur-md transition-all ${
        variantStyles[variant] || variantStyles.cyan
      } ${sizeStyles[size] || sizeStyles.md} ${className}`}
    >
      {dot && <span className={`w-1.5 h-1.5 rounded-full ${dotColors[variant] || dotColors.cyan}`} />}
      {children}
    </span>
  );
}

export default Badge;
