import React, { useEffect } from 'react';
import { CheckCircle2, AlertCircle, Info, X } from 'lucide-react';

/**
 * Cyberpunk HUD Toast notification component.
 */
export function Toast({
  id,
  type = 'info',
  title,
  message,
  onClose,
  duration = 4000,
}) {
  useEffect(() => {
    if (!duration || !onClose) return;
    const timer = setTimeout(() => {
      onClose(id);
    }, duration);
    return () => clearTimeout(timer);
  }, [id, duration, onClose]);

  const icons = {
    success: <CheckCircle2 className="w-5 h-5 text-emerald-400" />,
    error: <AlertCircle className="w-5 h-5 text-rose-400" />,
    info: <Info className="w-5 h-5 text-cyan-400" />,
  };

  const borders = {
    success: 'border-emerald-500/30 shadow-[0_0_20px_rgba(16,185,129,0.15)]',
    error: 'border-rose-500/30 shadow-[0_0_20px_rgba(244,63,94,0.15)]',
    info: 'border-cyan-500/30 shadow-[0_0_20px_rgba(6,182,212,0.15)]',
  };

  return (
    <div
      className={`flex items-start gap-3 p-4 rounded-xl bg-[#0e0e18]/90 border backdrop-blur-xl transition-all max-w-sm ${
        borders[type] || borders.info
      }`}
    >
      <div className="mt-0.5">{icons[type] || icons.info}</div>
      <div className="flex-1">
        {title && <h4 className="text-sm font-semibold text-white mb-0.5">{title}</h4>}
        {message && <p className="text-xs text-gray-300 leading-relaxed">{message}</p>}
      </div>
      {onClose && (
        <button
          onClick={() => onClose(id)}
          className="text-gray-400 hover:text-white transition-colors"
        >
          <X className="w-4 h-4" />
        </button>
      )}
    </div>
  );
}

export default Toast;
