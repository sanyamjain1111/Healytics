import './globals.css';
import Link from 'next/link';
import { NavLink } from '@/components/NavLink';

export const metadata = {
  title: 'Medical IntelliAnalytics Pro',
  description: 'Upload datasets, generate strategies, run ad‑hoc predictions & SQL',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <div className="container">
          <header style={{display:'flex',justifyContent:'space-between',alignItems:'center',margin:'12px 0 22px'}}>
            <div style={{display:'flex',gap:12,alignItems:'center'}}>
              <div className="badge"><b>IntelliAnalytics</b> v1</div>
            </div>
            <nav style={{display:'flex',gap:8}}>
              <NavLink href="/" exact>Home</NavLink>
              <NavLink href="/datasets">Datasets</NavLink>
              <NavLink href="/strategy">Strategy</NavLink>
              <NavLink href="/adhoc">Ad‑hoc</NavLink>
              <NavLink href="/sql">SQL</NavLink>
            </nav>
          </header>
          {children}
          <footer>© {new Date().getFullYear()} IntelliAnalytics • UI demo</footer>
        </div>
      </body>
    </html>
  );
}
