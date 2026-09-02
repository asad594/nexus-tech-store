import { useState, useEffect, useRef } from 'react';

/**
 * Custom React hook to track window scroll coordinates, scroll direction,
 * and boundary thresholds (isAtTop, isAtBottom).
 *
 * @param {number} throttleMs - Throttle limit for scroll updates (default: 50ms).
 * @returns {{
 *   x: number,
 *   y: number,
 *   direction: 'up' | 'down' | 'none',
 *   isAtTop: boolean,
 *   isAtBottom: boolean
 * }}
 */
export function useScrollPosition(throttleMs = 50) {
  const [scrollData, setScrollData] = useState({
    x: 0,
    y: 0,
    direction: 'none',
    isAtTop: true,
    isAtBottom: false,
  });

  const lastScrollY = useRef(0);
  const throttleTimeout = useRef(null);

  useEffect(() => {
    const handleScroll = () => {
      if (throttleTimeout.current) return;

      throttleTimeout.current = setTimeout(() => {
        const currentY = window.scrollY || document.documentElement.scrollTop;
        const currentX = window.scrollX || document.documentElement.scrollLeft;
        const scrollHeight = document.documentElement.scrollHeight;
        const clientHeight = document.documentElement.clientHeight;

        let dir = 'none';
        if (currentY > lastScrollY.current) {
          dir = 'down';
        } else if (currentY < lastScrollY.current) {
          dir = 'up';
        }

        lastScrollY.current = currentY;

        setScrollData({
          x: currentX,
          y: currentY,
          direction: dir,
          isAtTop: currentY <= 10,
          isAtBottom: currentY + clientHeight >= scrollHeight - 20,
        });

        throttleTimeout.current = null;
      }, throttleMs);
    };

    window.addEventListener('scroll', handleScroll, { passive: true });

    return () => {
      window.removeEventListener('scroll', handleScroll);
      if (throttleTimeout.current) {
        clearTimeout(throttleTimeout.current);
      }
    };
  }, [throttleMs]);

  return scrollData;
}

export default useScrollPosition;
