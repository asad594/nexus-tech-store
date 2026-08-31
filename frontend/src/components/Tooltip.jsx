import React, { useState, useRef } from 'react';

/**
 * Accessible Dark Glassmorphism Tooltip component for hover/focus hints.
 *
 * @param {React.ReactNode} children - The trigger element.
 * @param {string|React.ReactNode} content - The tooltip hint text/content.
 * @param {'top' | 'bottom' | 'left' | 'right'} position - Placement of the tooltip (default: 'top').
 * @param {number} delay - Display delay in milliseconds (default: 150).
 * @param {string} className - Optional wrapper styling.
 */
export function Tooltip({
  children,
  content,
  position = 'top',
  delay = 150,
  className = '',
}) {
  const [isVisible, setIsVisible] = useState(false);
  const timeoutRef = useRef(null);

  if (!content) {
    return <>{children}</>;
  }

  const showTooltip = () => {
    timeoutRef.current = setTimeout(() => {
      setIsVisible(true);
    }, delay);
  };

  const hideTooltip = () => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }
    setIsVisible(false);
  };

  const positionClasses = {
    top: 'bottom-full left-1/2 -translate-x-1/2 mb-2',
    bottom: 'top-full left-1/2 -translate-x-1/2 mt-2',
    left: 'right-full top-1/2 -translate-y-1/2 mr-2',
    right: 'left-full top-1/2 -translate-y-1/2 ml-2',
  };

  const arrowClasses = {
    top: 'top-full left-1/2 -translate-x-1/2 border-t-cyan-500/30 border-r-transparent border-b-transparent border-l-transparent',
    bottom: 'bottom-full left-1/2 -translate-x-1/2 border-b-cyan-500/30 border-r-transparent border-t-transparent border-l-transparent',
    left: 'left-full top-1/2 -translate-y-1/2 border-l-cyan-500/30 border-t-transparent border-r-transparent border-b-transparent',
    right: 'right-full top-1/2 -translate-y-1/2 border-r-cyan-500/30 border-t-transparent border-l-transparent border-b-transparent',
  };

  return (
    <div
      className={`relative inline-flex ${className}`}
      onMouseEnter={showTooltip}
      onMouseLeave={hideTooltip}
      onFocus={showTooltip}
      onBlur={hideTooltip}
    >
      {children}

      {isVisible && (
        <div
          role="tooltip"
          className={`absolute z-50 px-2.5 py-1 text-xs font-medium text-gray-200 bg-neutral-900/90 backdrop-blur-md border border-cyan-500/30 rounded-lg shadow-xl shadow-cyan-950/40 whitespace-nowrap pointer-events-none transition-all duration-200 animate-fadeIn ${
            positionClasses[position] || positionClasses.top
          }`}
        >
          {content}
          <span
            className={`absolute w-0 h-0 border-4 ${
              arrowClasses[position] || arrowClasses.top
            }`}
          />
        </div>
      )}
    </div>
  );
}

export default Tooltip;
