import { useEffect, useRef } from 'react';

/**
 * Declarative setInterval hook for React with automatic cleanup on unmount.
 * Passing `null` as delay pauses the interval.
 * @param {Function} callback - Function to execute on every tick.
 * @param {number|null} delay - Delay in milliseconds, or null to pause.
 */
export function useInterval(callback, delay) {
  const savedCallback = useRef(callback);

  useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);

  useEffect(() => {
    if (delay === null || delay === undefined) {
      return;
    }

    const tick = () => savedCallback.current();
    const id = setInterval(tick, delay);

    return () => clearInterval(id);
  }, [delay]);
}

export default useInterval;
