import { useEffect, useCallback } from 'react';

/**
 * Custom hook to detect when a specific key is pressed.
 * @param {string} targetKey - The key to listen for (e.g., 'Escape', 'Enter', 'k').
 * @param {Function} handler - Callback invoked when the key is pressed.
 * @param {Object} options - Configuration options (modifier keys, preventDefault).
 */
export function useKeyPress(targetKey, handler, options = {}) {
  const { ctrl = false, alt = false, shift = false, meta = false, preventDefault = false } = options;

  const handleKeyDown = useCallback(
    (event) => {
      const isKeyMatch = event.key.toLowerCase() === targetKey.toLowerCase();
      const isCtrlMatch = !ctrl || event.ctrlKey;
      const isAltMatch = !alt || event.altKey;
      const isShiftMatch = !shift || event.shiftKey;
      const isMetaMatch = !meta || event.metaKey;

      if (isKeyMatch && isCtrlMatch && isAltMatch && isShiftMatch && isMetaMatch) {
        if (preventDefault) {
          event.preventDefault();
        }
        handler(event);
      }
    },
    [targetKey, handler, ctrl, alt, shift, meta, preventDefault]
  );

  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [handleKeyDown]);
}

/**
 * Custom hook to bind multiple keyboard shortcuts in a single declaration.
 * @param {Array<{ key: string, handler: Function, options?: Object }>} keyMap
 */
export function useHotkeys(keyMap = []) {
  useEffect(() => {
    const handleKeyDown = (event) => {
      for (const { key, handler, options = {} } of keyMap) {
        const isKeyMatch = event.key.toLowerCase() === key.toLowerCase();
        const isCtrlMatch = !options.ctrl || event.ctrlKey;
        const isAltMatch = !options.alt || event.altKey;
        const isShiftMatch = !options.shift || event.shiftKey;
        const isMetaMatch = !options.meta || event.metaKey;

        if (isKeyMatch && isCtrlMatch && isAltMatch && isShiftMatch && isMetaMatch) {
          if (options.preventDefault) {
            event.preventDefault();
          }
          handler(event);
          break;
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [keyMap]);
}

export default useKeyPress;
