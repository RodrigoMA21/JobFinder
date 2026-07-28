import { Link } from 'react-router-dom';
import { useJobs } from '../hooks/useJobs';
import { JobCard } from '../components/jobs/JobCard';

export function Home() {
  const { data, isLoading } = useJobs({ per_page: 6, sort_by: 'published_at', sort_order: 'desc' });

  return (
    <div>
      <section className="border-b border-[var(--color-border)] bg-[var(--color-surface)]">
        <div className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl font-bold tracking-tight sm:text-5xl">
            Encontre a{' '}
            <span className="text-[var(--color-primary)]">vaga ideal</span>
          </h1>
          <p className="mx-auto mt-4 max-w-2xl text-lg text-[var(--color-text-secondary)]">
            Milhares de oportunidades de emprego reunidas em um só lugar.
            Pesquise por cargo, tecnologia, empresa ou localização.
          </p>
          <div className="mt-8 flex items-center justify-center gap-4">
            <Link
              to="/search"
              className="rounded-lg bg-[var(--color-primary)] px-8 py-3 text-sm font-semibold text-white hover:bg-[var(--color-primary-hover)] transition-colors"
            >
              Ver Todas as Vagas
            </Link>
            <Link
              to="/search?modality=remote"
              className="rounded-lg border border-[var(--color-border)] px-8 py-3 text-sm font-semibold text-[var(--color-text)] hover:bg-[var(--color-surface-secondary)] transition-colors"
            >
              Vagas Remotas
            </Link>
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="mb-8 flex items-center justify-between">
          <h2 className="text-2xl font-bold">Últimas Vagas</h2>
          <Link
            to="/search"
            className="text-sm font-medium text-[var(--color-primary)] hover:underline"
          >
            Ver Todas as Vagas →
          </Link>
        </div>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {isLoading &&
            Array.from({ length: 6 }).map((_, i) => (
              <div
                key={i}
                className="animate-pulse rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-5 space-y-3"
              >
                <div className="h-5 w-3/4 rounded bg-[var(--color-border)]" />
                <div className="h-4 w-1/3 rounded bg-[var(--color-border)]" />
                <div className="h-5 w-16 rounded-full bg-[var(--color-border)]" />
              </div>
            ))}
          {data?.data.map((job) => (
            <JobCard key={job.id} job={job} />
          ))}
        </div>
      </section>

      <section className="border-t border-[var(--color-border)] bg-[var(--color-surface)]">
        <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
          <div className="grid gap-8 sm:grid-cols-3 text-center">
            <div>
              <p className="text-3xl font-bold text-[var(--color-primary)]">
                {data?.meta.total || 'Milhares'}
              </p>
              <p className="mt-1 text-sm text-[var(--color-text-secondary)]">
                Vagas publicadas
              </p>
            </div>
            <div>
              <p className="text-3xl font-bold text-[var(--color-primary)]">+10</p>
              <p className="mt-1 text-sm text-[var(--color-text-secondary)]">
                Fontes de vagas
              </p>
            </div>
            <div>
              <p className="text-3xl font-bold text-[var(--color-primary)]">100%</p>
              <p className="mt-1 text-sm text-[var(--color-text-secondary)]">
                Gratuito
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
