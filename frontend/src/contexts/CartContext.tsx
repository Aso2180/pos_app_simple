import { createContext, useContext, useState } from 'react';

export type CartItem = {
  prd_id: number;
  code: string;
  name: string;
  price_ex_tax: number;
  price_in_tax: number;
  quantity: number;
};

type CartContextType = {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  clear: () => void;
};

const CartContext = createContext<CartContextType | null>(null);

export const CartProvider = ({ children }: { children: React.ReactNode }) => {
  const [items, setItems] = useState<CartItem[]>([]);

  const addItem = (item: CartItem) =>
    setItems((prev) => {
      const idx = prev.findIndex((i) => i.prd_id === item.prd_id);
      if (idx === -1) {
        //　新規追加
        return [...prev, item];
      }
        const next = [...prev];
        const newQty = next[idx].quantity + item.quantity;

      if (newQty <= 0) {
        // ★ 数量が 0 以下なら削除
        next.splice(idx, 1);
        return next;
      }

      next[idx] = { ...next[idx], quantity: newQty };
      return next;
    });

  const clear = () => setItems([]);

  return (
    <CartContext.Provider value={{ items, addItem, clear }}>
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => {
  const ctx = useContext(CartContext);
  if (!ctx) throw new Error('useCart must be inside <CartProvider>');
  return ctx;
};
