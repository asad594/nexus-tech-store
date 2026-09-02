import { useEffect, useRef } from 'react';

/**
 * Custom React hook to track the previous value of a prop or state variable across renders.
 * Useful for transition animations, value comparison, and change detections.
 *
 * @template T
 * @param {T} value - Current value to track.
 * @returns {T | undefined} The value from the previous render.
 */
export function usePrevious(value) {
  const ref = useRef();

  useEffect(() => {
    ref.current = value;
  }, [value]);

  return ref.current;
}

export default usePrevious;
