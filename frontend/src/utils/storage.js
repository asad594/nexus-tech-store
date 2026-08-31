/**
 * Robust, SSR-safe localStorage and sessionStorage wrapper with TTL expiration
 * and in-memory fallback for private browsing mode.
 */

class MemoryStorage {
  constructor() {
    this.store = new Map();
  }

  getItem(key) {
    return this.store.has(key) ? this.store.get(key) : null;
  }

  setItem(key, value) {
    this.store.set(key, String(value));
  }

  removeItem(key) {
    this.store.delete(key);
  }

  clear() {
    this.store.clear();
  }
}

const memoryFallback = new MemoryStorage();

function getStorageInstance(type = 'local') {
  try {
    const storage = type === 'session' ? window.sessionStorage : window.localStorage;
    const testKey = '__nexus_storage_test__';
    storage.setItem(testKey, '1');
    storage.removeItem(testKey);
    return storage;
  } catch {
    return memoryFallback;
  }
}

/**
 * Retrieves a value from storage, parsing JSON and checking TTL expiration.
 * @param {string} key
 * @param {any} defaultValue
 * @param {'local' | 'session'} storageType
 * @returns {any}
 */
export function safeGet(key, defaultValue = null, storageType = 'local') {
  const storage = getStorageInstance(storageType);
  try {
    const raw = storage.getItem(key);
    if (!raw) return defaultValue;

    const parsed = JSON.parse(raw);

    // Check TTL expiration if item is wrapped
    if (parsed && typeof parsed === 'object' && '__nexus_ttl__' in parsed) {
      if (Date.now() > parsed.__nexus_ttl__) {
        storage.removeItem(key);
        return defaultValue;
      }
      return parsed.data;
    }

    return parsed;
  } catch {
    return defaultValue;
  }
}

/**
 * Persists a value to storage with optional expiration duration.
 * @param {string} key
 * @param {any} value
 * @param {number|null} ttlMs - Expiration in milliseconds.
 * @param {'local' | 'session'} storageType
 * @returns {boolean} Success status.
 */
export function safeSet(key, value, ttlMs = null, storageType = 'local') {
  const storage = getStorageInstance(storageType);
  try {
    let payload = value;
    if (ttlMs && typeof ttlMs === 'number') {
      payload = {
        data: value,
        __nexus_ttl__: Date.now() + ttlMs,
      };
    }
    storage.setItem(key, JSON.stringify(payload));
    return true;
  } catch (error) {
    console.warn(`[NexusStorage] Failed to persist key "${key}":`, error);
    return false;
  }
}

/**
 * Removes an item from storage.
 * @param {string} key
 * @param {'local' | 'session'} storageType
 */
export function safeRemove(key, storageType = 'local') {
  const storage = getStorageInstance(storageType);
  try {
    storage.removeItem(key);
  } catch {}
}

/**
 * Clears items matching a key prefix.
 * @param {string} prefix
 * @param {'local' | 'session'} storageType
 */
export function clearByPrefix(prefix = 'nexus_', storageType = 'local') {
  const storage = getStorageInstance(storageType);
  try {
    if (storage instanceof MemoryStorage) {
      for (const key of storage.store.keys()) {
        if (key.startsWith(prefix)) storage.removeItem(key);
      }
      return;
    }

    Object.keys(storage)
      .filter((k) => k.startsWith(prefix))
      .forEach((k) => storage.removeItem(k));
  } catch {}
}
