import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import { fetchTransaction } from '@/lib/api';

export default function HistoryPage() {
  const router = useRouter();
  const id = Number(router.query.id);
  const [trn, setTrn] = useState<any | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    fetchTransaction(id)
      .then(setTrn)
      .catch(() => setError('取引が見つかりません'));
  }, [id]);

  if (error) return <p>{error}</p>;
  if (!trn) return <p>loading...</p>;

  return (
    <div style={{ padding: 20 }}>
      <h2>取引履歴 ID: {trn.transaction_id}</h2>
      <table border={1} cellPadding={6}>
        <thead>
          <tr>
            <th>商品名</th>
            <th>数量</th>
            <th>単価(税抜)</th>
            <th>金額</th>
          </tr>
        </thead>
        <tbody>
          {trn.items.map((l: any, idx: number) => (
            <tr key={idx}>
              <td>{l.prd_name}</td>
              <td>{l.quantity}</td>
              <td>¥{l.price_in_tax.toLocaleString()}</td>
              <td>¥{l.line_amount.toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <p style={{ fontWeight: 'bold' }}>
        合計(税抜) ¥{trn.total_amount_ex.toLocaleString()} / 合計(税込) ¥
        {trn.total_amount.toLocaleString()}
      </p>
      <button onClick={() => router.push('/pos')}>← POS に戻る</button>
    </div>
  );
}
