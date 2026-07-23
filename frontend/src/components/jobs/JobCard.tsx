import { Link } from 'react-router-dom';
import { Badge } from '../ui/Badge';
import type { JobSummary } from '../../types';

interface JobCardProps {
  job: JobSummary;
}

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

function timeAgo(date: string | null): string {
  if (!date) return '';
  const diff = Date.now() - new Date(date).getTime();
  const hours = Math.floor(diff / (1000 * 60 * 60));
  if (hours < 1) return 'Agora mesmo';
  if (hours < 24) return `Há ${hours}h`;
  const days = Math.floor(hours / 24);
  if (days < 30) return `Há ${days}d`;
  return new Date(date).toLocaleDateString('pt-BR');
}

export function JobCard({ job }: JobCardProps) {
  return (
    <Link
      to={`/jobs/${job.id}`}
      className="group block rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-5 transition-all hover:shadow-md hover:border-[var(--color-primary)]"
    >
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0 flex-1">
          <h3 className="text-lg font-semibold text-[var(--color-text)] group-hover:text-[var(--color-primary)] transition-colors truncate">
            {job.title}
          </h3>
          <p className="mt-1 text-sm text-[var(--color-text-secondary)]">
            {job.company.name}
            {job.city && ` — ${job.city}${job.state ? `, ${job.state}` : ''}`}
          </p>
        </div>
        {job.company.logo_url && (
          <img
            src={job.company.logo_url}
            alt={job.company.name}
            className="h-10 w-10 rounded-lg object-contain"
          />
        )}
      </div>

      <div className="mt-3 flex flex-wrap gap-2">
        <Badge variant="primary">{modalityLabels[job.modality]}</Badge>
        <Badge variant="success">{contractLabels[job.contract_type]}</Badge>
        <Badge variant="warning">{levelLabels[job.level]}</Badge>
      </div>

      <p className="mt-3 text-sm font-medium text-[var(--color-text)]">
        {formatSalary(job.salary_min, job.salary_max, job.currency)}
      </p>

      {job.technologies.length > 0 && (
        <div className="mt-3 flex flex-wrap gap-1.5">
          {job.technologies.slice(0, 5).map((tech) => (
            <span
              key={tech.id}
              className="rounded-md bg-[var(--color-primary-light)] px-2 py-0.5 text-xs font-medium text-[var(--color-primary)]"
            >
              {tech.name}
            </span>
          ))}
          {job.technologies.length > 5 && (
            <span className="text-xs text-[var(--color-text-muted)]">
              +{job.technologies.length - 5}
            </span>
          )}
        </div>
      )}

      <p className="mt-3 text-xs text-[var(--color-text-muted)]">
        {timeAgo(job.published_at)}
      </p>
    </Link>
  );
}
