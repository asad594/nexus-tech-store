import React, { useState } from 'react';
import { ChevronDown } from 'lucide-react';

/**
 * Single Collapsible Item for Accordion.
 */
export function AccordionItem({
  title,
  children,
  isOpen = false,
  onToggle = () => {},
  badge,
  className = '',
}) {
  return (
    <div
      className={`border border-white/10 rounded-xl overflow-hidden bg-neutral-900/60 backdrop-blur-md transition-colors ${
        isOpen ? 'border-cyan-500/40 shadow-lg shadow-cyan-950/20' : 'hover:border-white/20'
      } ${className}`}
    >
      <button
        type="button"
        onClick={onToggle}
        className="flex items-center justify-between w-full px-5 py-4 text-left cursor-pointer focus:outline-none focus-visible:ring-1 focus-visible:ring-cyan-400"
        aria-expanded={isOpen}
      >
        <div className="flex items-center gap-3">
          <span className="text-sm font-semibold text-gray-100">{title}</span>
          {badge && (
            <span className="px-2 py-0.5 text-2xs font-semibold uppercase tracking-wider text-cyan-400 bg-cyan-950/50 border border-cyan-500/30 rounded-full">
              {badge}
            </span>
          )}
        </div>
        <ChevronDown
          className={`w-4 h-4 text-gray-400 transition-transform duration-200 ${
            isOpen ? 'rotate-180 text-cyan-400' : ''
          }`}
        />
      </button>

      {isOpen && (
        <div className="px-5 pb-5 pt-1 text-sm text-gray-400 border-t border-white/5 animate-fadeIn">
          {children}
        </div>
      )}
    </div>
  );
}

/**
 * Accordion container supporting single or multiple open items.
 *
 * @param {Array<{ id: string|number, title: string, content: React.ReactNode, badge?: string }>} items
 * @param {boolean} allowMultiple - Whether multiple sections can be open simultaneously.
 * @param {string} className - Optional container styling.
 */
export function Accordion({ items = [], allowMultiple = false, className = '' }) {
  const [openIds, setOpenIds] = useState(new Set());

  const handleToggle = (id) => {
    setOpenIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        if (!allowMultiple) next.clear();
        next.add(id);
      }
      return next;
    });
  };

  return (
    <div className={`flex flex-col gap-3 ${className}`}>
      {items.map((item) => (
        <AccordionItem
          key={item.id}
          title={item.title}
          badge={item.badge}
          isOpen={openIds.has(item.id)}
          onToggle={() => handleToggle(item.id)}
        >
          {item.content}
        </AccordionItem>
      ))}
    </div>
  );
}

export default Accordion;
