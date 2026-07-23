import { useParams, Link } from 'react-router-dom';
import { useJob } from '../hooks/useJobs';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { Skeleton } from '../components/ui/Skeleton';

const modalityLabels: Record<string, string> = {
  remote: 'Remoto',
  hybrid: 'Híbrido',
  onsite: 'Presencial',
};

const contractLabels: Record<string, string> = {
  clt: 'CLT',
  pj: 'PJ',
  freelancer: 'Freelancer',
  internship: 'Estágio',
};

const levelLabels: Record<string, string> = {
  internship: 'Estágio',
  junior: 'Júnior',
  mid: 'Pleno',
  senior: 'Sênior',
};

function formatSalary(min: number | null, max: number | null, currency: string): string {
  if (min === null && max === null) return 'A combinar';
  const fmt = (v: number) =>
    new Intl.NumberFormat('pt-BR', { style: 'currency', currency }).format(v);
  if (min !== null && max !== null) return `${fmt(min)} - ${fmt(max)}`;
  if (min !== null) return `A partir de ${fmt(min)}`;
  return `Até ${fmt(max!)}`;
}

export function JobDetails() {
  const { id } = useParams<{ id: string }>();
  const { data, isLoading, isError } = useJob(id!);

  if (isLoading) {
    return (
      <div className="mx-auto max-w-4xl px-4 py-8 sm:px-6 lg:px-8 space-y-6">
        <Skeleton className="h-8 w-2/3" />
        <Skeleton className="h-5 w-1/3" />
        <div className="flex gap-2">
          <Skeleton className="h-6 w-20 rounded-full" />
          <Skeleton className="h-6 w-20 rounded-full" />
          <Skeleton className="h-6 w-20 rounded-full" />
        </div>
        <Skeleton className="h-64 w-full" />
      </div>
    );
  }

  if (isError || !data?.data) {
    return (
      <div className="mx-auto max-w-4xl px-4 py-20 text-center">
        <h2 className="text-2xl font-bold">Vaga não encontrada</h2>
        <p className="mt-2 text-[var(--color-text-secondary)]">
          A vaga que você procura não existe ou foi removida.
        </p>
        <Link
          to="/search"
          className="mt-6 inline-block text-[var(--color-primary)] hover:underline"
        >
          ← Voltar para busca
        </Link>
      </div>
    );
  }

  const job = data.data;

  return (
    <div className="mx-auto max-w-4xl px-4 py-8 sm:px-6 lg:px-8">
      <Link
        to="/search"
        className="mb-6 inline-flex items-center gap-1 text-sm text-[var(--color-text-secondary)] hover:text-[var(--color-text)] transition-colors"
      >
        <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
        </svg>
        Voltar para resultados
      </Link>

      <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-6 sm:p-8">
        <div className="flex items-start justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold sm:text-3xl">{job.title}</h1>
            <p className="mt-2 text-lg text-[var(--color-text-secondary)]">
              {job.company.name}
              {job.city && ` — ${job.city}${job.state ? `, ${job.state}` : ''}`}
            </p>
          </div>
          {job.company.logo_url && (
            <img
              src={job.company.logo_url}
              alt={job.company.name}
              className="h-14 w-14 rounded-xl object-contain"
            />
          )}
        </div>

        <div className="mt-6 flex flex-wrap gap-2">
          <Badge variant="primary">{modalityLabels[job.modality]}</Badge>
          <Badge variant="success">{contractLabels[job.contract_type]}</Badge>
          <Badge variant="warning">{levelLabels[job.level]}</Badge>
        </div>

        <p className="mt-4 text-xl font-semibold">
          {formatSalary(job.salary_min, job.salary_max, job.currency)}
        </p>

        {job.technologies.length > 0 && (
          <div className="mt-4">
            <h3 className="text-sm font-medium text-[var(--color-text-secondary)] mb-2">
              Tecnologias
            </h3>
            <div className="flex flex-wrap gap-2">
              {job.technologies.map((tech) => (
                <span
                  key={tech.id}
                  className="rounded-lg bg-[var(--color-primary-light)] px-3 py-1 text-sm font-medium text-[var(--color-primary)]"
                >
                  {tech.name}
                </span>
              ))}
            </div>
          </div>
        )}

        <div className="mt-8 space-y-6">
          <div>
            <h2 className="text-lg font-semibold mb-3">Descrição</h2>
            <div
              className="prose prose-sm max-w-none text-[var(--color-text-secondary)] [&_a]:text-[var(--color-primary)]"
              dangerouslySetInnerHTML={{ __html: job.description }}
            />
          </div>

          {job.requirements && (
            <div>
              <h2 className="text-lg font-semibold mb-3">Requisitos</h2>
              <div
                className="prose prose-sm max-w-none text-[var(--color-text-secondary)]"
                dangerouslySetInnerHTML={{ __html: job.requirements }}
              />
            </div>
          )}

          {job.benefits && (
            <div>
              <h2 className="text-lg font-semibold mb-3">Benefícios</h2>
              <div
                className="prose prose-sm max-w-none text-[var(--color-text-secondary)]"
                dangerouslySetInnerHTML={{ __html: job.benefits }}
              />
            </div>
          )}
        </div>

        <div className="mt-8 flex items-center justify-between border-t border-[var(--color-border)] pt-6">
          <p className="text-sm text-[var(--color-text-muted)]">
            Publicado em{' '}
            {job.published_at
              ? new Date(job.published_at).toLocaleDateString('pt-BR')
              : 'data não informada'}
          </p>
          <a
            href={job.application_url || '#'}
            target="_blank"
            rel="noopener noreferrer"
          >
            <Button>
              Candidatar-se
              <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 6H5.25A2.25 2.25 0 003 8.25v10.5A2.25 2.25 0 005.25 21h10.5A2.25 2.25 0 0018 18.75V10.5m-10.5 6L21 3m0 0h-5.25M21 3v5.25" />
              </svg>
            </Button>
          </a>
        </div>
      </div>
    </div>
  );
}
