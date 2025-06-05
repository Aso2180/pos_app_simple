import Link from 'next/link';

export default function Home() {
  return (
    <div style={{ padding: 20 }}>
      <h1>POS Frontend (Minimal)</h1>
      <Link href="/pos">→ POS 画面へ</Link>
    </div>
  );
}
