import { useState, useEffect, useCallback } from 'react';

/**
 * Custom React hook to track real-time network connectivity and browser online/offline status.
 *
 * @returns {{
 *   isOnline: boolean,
 *   wasOffline: boolean,
 *   connectionType: string|null,
 *   recheckConnection: () => Promise<boolean>
 * }}
 */
export function useOnlineStatus() {
  const [isOnline, setIsOnline] = useState(() =>
    typeof navigator !== 'undefined' && typeof navigator.onLine === 'boolean'
      ? navigator.onLine
      : true
  );
  const [wasOffline, setWasOffline] = useState(false);
  const [connectionType, setConnectionType] = useState(() => {
    if (typeof navigator !== 'undefined' && navigator.connection) {
      return navigator.connection.effectiveType || null;
    }
    return null;
  });

  const recheckConnection = useCallback(async () => {
    if (typeof navigator !== 'undefined' && typeof navigator.onLine === 'boolean') {
      const online = navigator.onLine;
      setIsOnline(online);
      return online;
    }
    return true;
  }, []);

  useEffect(() => {
    const handleOnline = () => {
      setIsOnline(true);
    };

    const handleOffline = () => {
      setIsOnline(false);
      setWasOffline(true);
    };

    const handleConnectionChange = () => {
      if (navigator.connection) {
        setConnectionType(navigator.connection.effectiveType || null);
      }
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    if (navigator.connection) {
      navigator.connection.addEventListener('change', handleConnectionChange);
    }

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
      if (navigator.connection) {
        navigator.connection.removeEventListener('change', handleConnectionChange);
      }
    };
  }, []);

  return {
    isOnline,
    wasOffline,
    connectionType,
    recheckConnection,
  };
}

export default useOnlineStatus;
