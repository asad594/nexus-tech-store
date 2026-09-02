import { useState, useCallback } from 'react';

/**
 * Custom hook to handle boolean state with declarative helper actions.
 *
 * @param {boolean} initialValue - Initial state value (default: false).
 * @returns {[boolean, () => void, (val?: boolean) => void, () => void, () => void]}
 *   [value, toggle, setValue, setTrue, setFalse]
 */
export function useToggle(initialValue = false) {
  const [value, setValue] = useState(Boolean(initialValue));

  const toggle = useCallback(() => {
    setValue((prev) => !prev);
  }, []);

  const setTrue = useCallback(() => {
    setValue(true);
  }, []);

  const setFalse = useCallback(() => {
    setValue(false);
  }, []);

  return [value, toggle, setValue, setTrue, setFalse];
}

export default useToggle;
