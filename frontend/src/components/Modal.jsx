import React, { useEffect } from 'react';
import { X } from 'lucide-react';

/**
 * Accessible Dark Glassmorphism Modal presentation wrapper with backdrop blur,
 * keyboard escape listener, and outside click dismissal.
 *
 * @param {boolean} isOpen - Modal visibility state.
 * @param {Function} onClose - Callback invoked to close modal.
 * @param {string} title - Optional header title text.
 * @param {React.ReactNode} children - Modal body content.
 * @param {'sm' | 'md' | 'lg' | 'xl' | 'full'} size - Max width sizing.
 * @param {string} className - Optional modal styling classes.
 */
export function Modal({
  isOpen,
  onClose,
  title,
  children,
  size = 'md',
  className = '',
}) {
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };

    if (isOpen) {
      document.body.style.overflow = 'hidden';
      window.addEventListener('keydown', handleKeyDown);
    }

    return () => {
      document.body.style.overflow = '';
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const sizeClasses = {
    sm: 'max-w-md',
    md: 'max-w-lg',
    lg: 'max-w-2xl',
    xl: 'max-w-4xl',
    full: 'max-w-6xl',
  };

  return (
    <div
      role="dialog"
      aria-modal="true"
      className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6"
    >
      {/* Backdrop */}
      <div
        onClick={onClose}
        className="fixed inset-0 bg-black/80 backdrop-blur-md transition-opacity animate-fadeIn"
      />

      {/* Modal Container */}
      <div
        className={`relative w-full ${
          sizeClasses[size] || sizeClasses.md
        } bg-neutral-900/95 border border-cyan-500/30 rounded-2xl shadow-2xl shadow-cyan-950/50 backdrop-blur-xl overflow-hidden z-10 animate-scaleUp ${className}`}
      >
        {/* Header */}
        {(title || onClose) && (
          <div className="flex items-center justify-between px-6 py-4 border-b border-white/10">
            {title && (
              <h3 className="text-lg font-bold text-gray-100 tracking-wide">{title}</h3>
            )}
            {onClose && (
              <button
                type="button"
                onClick={onClose}
                aria-label="Close dialog"
                className="p-1 text-gray-400 hover:text-white hover:bg-white/10 rounded-lg transition-colors cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            )}
          </div>
        )}

        {/* Content Body */}
        <div className="p-6 max-h-[80vh] overflow-y-auto custom-scrollbar">
          {children}
        </div>
      </div>
    </div>
  );
}

export default Modal;
