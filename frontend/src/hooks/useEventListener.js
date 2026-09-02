import { useEffect, useRef } from 'react';

/**
 * Declarative hook for binding event listeners to Window, Document, or DOM Elements.
 * Automatically updates handler reference without needing to re-attach listeners.
 *
 * @param {string} eventName - Name of DOM event (e.g. 'resize', 'scroll', 'click').
 * @param {Function} handler - Event callback.
 * @param {RefObject|HTMLElement|Window|Document} element - Target element (defaults to window).
 * @param {boolean|AddEventListenerOptions} options - Optional listener options.
 */
export function useEventListener(eventName, handler, element = undefined, options = {}) {
  const savedHandler = useRef(handler);

  useEffect(() => {
    savedHandler.current = handler;
  }, [handler]);

  useEffect(() => {
    const targetElement = element?.current ?? element ?? (typeof window !== 'undefined' ? window : null);
    if (!targetElement || !targetElement.addEventListener) {
      return;
    }

    const eventListener = (event) => savedHandler.current?.(event);
    targetElement.addEventListener(eventName, eventListener, options);

    return () => {
      targetElement.removeEventListener(eventName, eventListener, options);
    };
  }, [eventName, element, options]);
}

export default useEventListener;
