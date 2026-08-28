import { useState, useCallback } from 'react';

/**
 * Custom hook to copy text to clipboard with feedback timer.
 */
export function useClipboard(timeout = 2000) {
  const [hasCopied, setHasCopied] = useState(false);

  const copy = useCallback(
    async (text) => {
      if (!navigator?.clipboard) {
        console.warn('Clipboard API not available in browser');
        return false;
      }

      try {
        await navigator.clipboard.writeText(text);
        setHasCopied(true);
        setTimeout(() => setHasCopied(false), timeout);
        return true;
      } catch (error) {
        console.warn('Failed to copy text:', error);
        setHasCopied(false);
        return false;
      }
    },
    [timeout]
  );

  return { copy, hasCopied };
}
