import { useEffect, useRef, useCallback } from 'react';

/**
 * Declarative setTimeout hook for React with reset/clear capabilities.
 * @param {Function} callback - Function to run once timer expires.
 * @param {number|null} delay - Delay in milliseconds, or null to cancel.
 * @returns {{ reset: Function, clear: Function }}
 */
export function useTimeout(callback, delay) {
  const callbackRef = useRef(callback);
  const timeoutRef = useRef(null);

  useEffect(() => {
    callbackRef.current = callback;
  }, [callback]);

  const set = useCallback(() => {
    if (delay !== null && delay !== undefined) {
      timeoutRef.current = setTimeout(() => callbackRef.current(), delay);
    }
  }, [delay]);

  const clear = useCallback(() => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }
  }, []);

  useEffect(() => {
    set();
    return clear;
  }, [delay, set, clear]);

  const reset = useCallback(() => {
    clear();
    set();
  }, [clear, set]);

  return { reset, clear };
}

export default useTimeout;
