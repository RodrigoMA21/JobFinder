import { Outlet } from 'react-router-dom';
import { Header } from './Header';
import { Footer } from './Footer';
import { MaintenanceBanner } from '../ui/MaintenanceBanner';

export function Layout() {
  return (
    <div className="flex min-h-screen flex-col">
      <MaintenanceBanner />
      <Header />
      <main className="flex-1">
        <Outlet />
      </main>
      <Footer />
    </div>
  );
}
