import React, { createContext, useContext, useState, useEffect } from 'react';
import { useAuth } from './AuthContext';
import API from '../api';

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

  const addToCart = async (product, quantity = 1) => {
    if (user) {
      try {
        await API.post('/cart/', { product: product.id, quantity });
        await fetchCart();
      } catch (err) {
        console.error('Error adding to cart', err);
      }
    } else {
      setCartItems(prev => {
        const existing = prev.find(item => item.product.id === product.id);
        if (existing) {
          return prev.map(item =>
            item.product.id === product.id
              ? { ...item, quantity: item.quantity + quantity }
              : item
          );
        }
        return [...prev, { id: Date.now(), product, quantity }];
      });
    }
    setIsCartOpen(true);
  };

  const updateQuantity = async (productId, newQty) => {
    if (newQty <= 0) {
      return removeFromCart(productId);
    }
    if (user) {
      const item = cartItems.find(i => i.product.id === productId);
      if (item) {
        try {
          await API.patch(`/cart/${item.id}/`, { quantity: newQty });
          await fetchCart();
        } catch (err) {
          console.error('Error updating cart item', err);
        }
      }
    } else {
      setCartItems(prev => prev.map(item =>
        item.product.id === productId ? { ...item, quantity: newQty } : item
      ));
    }
  };

  const removeFromCart = async (productId) => {
    if (user) {
      const item = cartItems.find(i => i.product.id === productId);
      if (item) {
        try {
          await API.delete(`/cart/${item.id}/`);
          await fetchCart();
        } catch (err) {
          console.error('Error deleting cart item', err);
        }
      }
    } else {
      setCartItems(prev => prev.filter(item => item.product.id !== productId));
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
  const subtotal = cartItems.reduce((acc, item) => acc + (parseFloat(item.product.price) * item.quantity), 0);

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
