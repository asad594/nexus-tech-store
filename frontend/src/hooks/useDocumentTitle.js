import { useEffect } from 'react';

/**
 * Custom hook to manage the browser tab title dynamically.
 */
export function useDocumentTitle(title, retainOnUnmount = false) {
  useEffect(() => {
    const previousTitle = document.title;
    if (title) {
      document.title = `${title} | Nexus Tech Store`;
    }

    return () => {
      if (!retainOnUnmount) {
        document.title = previousTitle;
      }
    };
  }, [title, retainOnUnmount]);
}
