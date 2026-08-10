import React, { createContext, useContext, useState, useEffect } from 'react';
import { useAuth } from './AuthContext';
import API from '../api';

/**
 * Shopping Cart Context providing synchronized state between guest
 * localStorage persistence and backend API persistence for authenticated users.
 */
const CartContext = createContext();

export const CartProvider = ({ children }) => {
  const [cartItems, setCartItems] = useState([]);
  const [isCartOpen, setIsCartOpen] = useState(false);
  const { user } = useAuth();

  const fetchCart = async () => {
    if (user) {
      try {
        const response = await API.get('/cart/');
        const formatted = response.data.map(item => ({
          id: item.id,
          product: item.product_detail,
          variant: item.variant_detail || null,
          quantity: item.quantity,
        }));
        setCartItems(formatted);
      } catch (err) {
        console.error('Failed to fetch backend cart', err);
      }
    } else {
      const saved = localStorage.getItem('nexus_local_cart');
      if (saved) {
        setCartItems(JSON.parse(saved));
      }
    }
  };

  useEffect(() => {
    fetchCart();
  }, [user]);

  useEffect(() => {
    if (!user) {
      localStorage.setItem('nexus_local_cart', JSON.stringify(cartItems));
    }
  }, [cartItems, user]);

  const addToCart = async (product, quantity = 1, variant = null) => {
    const selectedVariant = variant || (product.variants?.find(v => v.is_default) || product.variants?.[0] || null);

    if (user) {
      try {
        await API.post('/cart/', {
          product: product.id,
          variant: selectedVariant?.id || null,
          quantity
        });
        await fetchCart();
      } catch (err) {
        console.error('Error adding to cart', err);
      }
    } else {
      setCartItems(prev => {
        const existingIndex = prev.findIndex(item =>
          item.product.id === product.id &&
          ((!item.variant && !selectedVariant) || (item.variant?.id === selectedVariant?.id))
        );

        if (existingIndex > -1) {
          const updated = [...prev];
          updated[existingIndex] = {
            ...updated[existingIndex],
            quantity: updated[existingIndex].quantity + quantity
          };
          return updated;
        }

        return [...prev, {
          id: `local_${Date.now()}_${Math.random().toString(36).substr(2, 5)}`,
          product,
          variant: selectedVariant,
          quantity
        }];
      });
    }
    setIsCartOpen(true);
  };

  const updateQuantity = async (cartItemId, newQty) => {
    if (newQty <= 0) {
      return removeFromCart(cartItemId);
    }
    if (user) {
      try {
        await API.patch(`/cart/${cartItemId}/`, { quantity: newQty });
        await fetchCart();
      } catch (err) {
        console.error('Error updating cart item', err);
      }
    } else {
      setCartItems(prev => prev.map(item =>
        item.id === cartItemId ? { ...item, quantity: newQty } : item
      ));
    }
  };

  const removeFromCart = async (cartItemId) => {
    if (user) {
      try {
        await API.delete(`/cart/${cartItemId}/`);
        await fetchCart();
      } catch (err) {
        console.error('Error deleting cart item', err);
      }
    } else {
      setCartItems(prev => prev.filter(item => item.id !== cartItemId));
    }
  };

  const clearCart = async () => {
    if (user) {
      try {
        await API.delete('/cart/clear/');
      } catch (err) {
        console.error('Error clearing cart', err);
      }
    }
    setCartItems([]);
  };

  const totalItems = cartItems.reduce((acc, item) => acc + item.quantity, 0);
  const subtotal = cartItems.reduce((acc, item) => {
    const basePrice = parseFloat(item.product.price) || 0;
    const delta = item.variant?.price_delta ? parseFloat(item.variant.price_delta) : 0;
    return acc + ((basePrice + delta) * item.quantity);
  }, 0);

  return (
    <CartContext.Provider value={{
      cartItems,
      isCartOpen,
      setIsCartOpen,
      addToCart,
      updateQuantity,
      removeFromCart,
      clearCart,
      totalItems,
      subtotal,
      fetchCart
    }}>
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => useContext(CartContext);
