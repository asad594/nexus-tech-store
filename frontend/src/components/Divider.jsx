import React from 'react';

/**
 * Futuristic Glassmorphic Divider with glowing gradient accent lines.
 *
 * @param {string|React.ReactNode} label - Optional center badge or label text.
 * @param {'cyan' | 'purple' | 'amber' | 'neutral'} variant - Accent color theme.
 * @param {'horizontal' | 'vertical'} orientation - Line direction.
 * @param {string} className - Optional wrapper class names.
 */
export function Divider({
  label,
  variant = 'cyan',
  orientation = 'horizontal',
  className = '',
}) {
  const gradientClasses = {
    cyan: 'from-transparent via-cyan-500/40 to-transparent',
    purple: 'from-transparent via-purple-500/40 to-transparent',
    amber: 'from-transparent via-amber-500/40 to-transparent',
    neutral: 'from-transparent via-gray-700/50 to-transparent',
  };

  const glowClasses = {
    cyan: 'shadow-[0_0_12px_rgba(6,182,212,0.4)]',
    purple: 'shadow-[0_0_12px_rgba(168,85,247,0.4)]',
    amber: 'shadow-[0_0_12px_rgba(245,158,11,0.4)]',
    neutral: '',
  };

  if (orientation === 'vertical') {
    return (
      <div
        className={`inline-block w-[1px] self-stretch bg-gradient-to-b ${
          gradientClasses[variant] || gradientClasses.cyan
        } ${glowClasses[variant]} ${className}`}
      />
    );
  }

  if (label) {
    return (
      <div className={`relative flex items-center justify-center my-6 ${className}`}>
        <div
          className={`flex-grow h-[1px] bg-gradient-to-r ${
            gradientClasses[variant] || gradientClasses.cyan
          }`}
        />
        <span className="px-3 py-1 text-xs font-semibold text-gray-400 uppercase tracking-widest bg-neutral-900/90 border border-white/10 rounded-full backdrop-blur-md">
          {label}
        </span>
        <div
          className={`flex-grow h-[1px] bg-gradient-to-r ${
            gradientClasses[variant] || gradientClasses.cyan
          }`}
        />
      </div>
    );
  }

  return (
    <div
      className={`w-full h-[1px] my-6 bg-gradient-to-r ${
        gradientClasses[variant] || gradientClasses.cyan
      } ${glowClasses[variant]} ${className}`}
    />
  );
}

export default Divider;
