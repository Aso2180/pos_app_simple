import { useMemo, useState } from 'react';
import { useRouter } from 'next/router';        // ★ 追加
import { fetchProduct, createPurchase } from '@/lib/api';
import { useCart, CartProvider } from '@/contexts/CartContext';
import Modal from '@/components/Modal';

function PosInner() {
  const {items, addItem, clear } = useCart();
  const [code, setCode] = useState('');
  const [product, setProduct] = useState<any | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [dialog, setDialog] = useState<React.ReactNode | null>(null);
  const [pendingClear, setPendingClear] = useState(false);   // ★ 追加
  const [lastTid, setLastTid] = useState<number | null>(null);
  const router = useRouter();      // ★ 追加


  /* ---------- カート合計 ---------- */
  const { totalEx, totalIn } = useMemo(() => {
    let ex = 0,
      inc = 0;
    items.forEach((i) => {
      ex += i.price_ex_tax * i.quantity;
      inc += i.price_in_tax * i.quantity;
    });
    return { totalEx: ex, totalIn: inc };
  }, [items]);

  /* ---------- 検索 ---------- */
  const handleLookup = async () => {
    try {
      const p = await fetchProduct(code);
      setProduct(p);
      setError(null);
    } catch {
      setProduct(null);
      setError('商品が見つかりません');
    }
  };

  /* ---------- カート操作 ---------- */
  const handleAdd = () => {
    if (!product) return;
    addItem({ prd_id: product.id, ...product, quantity: 1 });
    setProduct(null);
    setCode('');
  };

  const adjustQty = (id: number, delta: number) => {
    addItem({ ...items.find((i) => i.prd_id === id)!, quantity: delta });
  };

  /* ---------- 購入 ---------- */
  const handlePurchase = async () => {
    if (!items.length) return;

    const payload = {
      emp_cd: '000001',
      items: items.map((i) => ({ prd_id: i.prd_id, quantity: i.quantity })),
    };

    try {
      const res = await createPurchase(payload);
    /*const tid = res.transaction_id;               // ★ スコープ内で保持 */
      setLastTid(res.transaction_id);              // ★ 追加

      setDialog(
        <>
          購入完了！<br />
          取引ID: {res.transaction_id}
          <br />
          合計(税抜) ¥{res.total_amount_ex.toLocaleString()} / 合計(税込){' '}
          ¥{res.total_amount.toLocaleString()}
        </>
      );
      setPendingClear(true);      // ← モーダル閉じ時にクリアする
    } catch (err: any) {
      setDialog(`購入エラー:\n${JSON.stringify(err.response?.data)}`);
    }
  };

  /* ---------- UI ---------- */
  return (
    <div style={{ padding: 20, maxWidth: 430 }}>
      <h2>POS 画面</h2>

      <input
        placeholder="バーコード / コード"
        value={code}
        onChange={(e) => setCode(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && handleLookup()}
        style={{ width: 220 }}
      />
      <button onClick={handleLookup}>読み込み</button>

      {product && (
        <>
          <p>名称: {product.name}</p>
          <p>単価: ¥{product.price_in_tax}</p>
          <button onClick={handleAdd}>カートに追加</button>
        </>
      )}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      <h3 style={{ marginTop: 25 }}>カート</h3>
      <ul>
        {items.map((i) => (
          <li key={i.prd_id}>
            {i.name} × {i.quantity} ＝ ¥
            {(i.price_in_tax * i.quantity).toLocaleString()}{' '}
            {/* +- ボタン */}
            <button onClick={() => adjustQty(i.prd_id, 1)}>＋</button>
            <button
              onClick={() => adjustQty(i.prd_id, -1)}>－</button>
          </li>
        ))}
      </ul>

      <p style={{ fontWeight: 'bold' }}>
        合計(税抜) ¥{totalEx.toLocaleString()} / (税込) ¥
        {totalIn.toLocaleString()}
      </p>

      <button disabled={!items.length} onClick={handlePurchase}>
        購入
      </button>

      {/* モーダル */}
      {dialog && (
        <Modal
          message={dialog}
          onClose={() => {
            setDialog(null);
            if (pendingClear) {
             clear();                // ★ ここでカートを空に
             setPendingClear(false);
            }
            if (lastTid) {
              router.push(`/history?id=${lastTid}`);  // ★ 履歴ページへ遷移
              setLastTid(null);
            }
          }}
        />
      )}
    </div>
  );
}

export default function PosPage() {
  return (
    <CartProvider>
      <PosInner />
    </CartProvider>
  );
}
