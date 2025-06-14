import axios from 'axios';

const baseURL = process.env.NEXT_PUBLIC_API_URL!;   // 「!」で必須を明示
export const api = axios.create({ baseURL });

// 商品取得
export const fetchProduct = (code: string) =>
  api.get(`/products/${code}`).then((r) => r.data);

// 購入登録 ― payload 一括で渡す
export const createPurchase = (payload: any) =>
  api.post('/purchase', payload).then((r) => r.data);

// 取引参照
export const fetchTransaction = (id: number) =>
  api.get(`/transactions/${id}`).then((r) => r.data);
