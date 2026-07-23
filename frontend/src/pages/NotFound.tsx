import { Link } from 'react-router-dom';

export function NotFound() {
  return (
    <div className="flex min-h-[calc(100vh-4rem)] flex-col items-center justify-center px-4 text-center">
      <div className="text-8xl font-bold text-[var(--color-primary)]">404</div>
      <h1 className="mt-4 text-2xl font-bold">Página não encontrada</h1>
      <p className="mt-2 text-[var(--color-text-secondary)]">
        A página que você procura não existe ou foi movida.
      </p>
      <Link
        to="/"
        className="mt-8 rounded-lg bg-[var(--color-primary)] px-6 py-3 text-sm font-semibold text-white hover:bg-[var(--color-primary-hover)] transition-colors"
      >
        Voltar ao início
      </Link>
    </div>
  );
}
