import { useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { FilterBar } from '../components/filters/FilterBar';
import { JobList } from '../components/jobs/JobList';
import { useJobs } from '../hooks/useJobs';
import { Button } from '../components/ui/Button';
import { triggerSync } from '../services/api';
import type { JobSearchParams } from '../services/api';

export function Search() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [syncing, setSyncing] = useState(false);

  const [params, setParams] = useState<JobSearchParams>(() => {
    const initial: JobSearchParams = {};
    for (const [key, value] of searchParams.entries()) {
      (initial as Record<string, string>)[key] = value;
    }
    return initial;
  });

  const { data, isLoading, isError, refetch } = useJobs(params);

  async function handleSync() {
    setSyncing(true);
    try {
      await triggerSync();
      refetch();
    } catch {
      // silent
    } finally {
      setSyncing(false);
    }
  }

  const handleChange = (newParams: JobSearchParams) => {
    setParams(newParams);
    const entries = Object.entries(newParams).filter(
      ([_, v]) => v !== undefined && v !== '' && v !== null
    );
    setSearchParams(entries);
  };

  const handleReset = () => {
    setParams({});
    setSearchParams({});
  };

  const handlePageChange = (page: number) => {
    handleChange({ ...params, page });
  };

  const currentPage = params.page || 1;
  const totalPages = data?.meta.total_pages || 0;

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-2xl font-bold">Buscar Vagas</h1>
        <Button variant="secondary" size="sm" onClick={handleSync} disabled={syncing}>
          {syncing ? (
            <>
              <svg className="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              Sincronizando...
            </>
          ) : (
            <>
              <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182" />
              </svg>
              Sincronizar vagas
            </>
          )}
        </Button>
      </div>

      <FilterBar params={params} onChange={handleChange} onReset={handleReset} />

      <div className="mt-6">
        <p className="mb-4 text-sm text-[var(--color-text-secondary)]">
          {data?.meta.total
            ? `${data.meta.total} vaga${data.meta.total !== 1 ? 's' : ''} encontrada${data.meta.total !== 1 ? 's' : ''}`
            : ''}
        </p>

        <JobList jobs={data?.data} isLoading={isLoading} isError={isError} />

        {totalPages > 1 && (
          <div className="mt-8 flex items-center justify-center gap-2">
            <Button
              variant="secondary"
              size="sm"
              disabled={currentPage <= 1}
              onClick={() => handlePageChange(currentPage - 1)}
            >
              Anterior
            </Button>
            {Array.from({ length: Math.min(totalPages, 5) }, (_, i) => {
              let pageNum: number;
              if (totalPages <= 5) {
                pageNum = i + 1;
              } else if (currentPage <= 3) {
                pageNum = i + 1;
              } else if (currentPage >= totalPages - 2) {
                pageNum = totalPages - 4 + i;
              } else {
                pageNum = currentPage - 2 + i;
              }
              return (
                <Button
                  key={pageNum}
                  variant={pageNum === currentPage ? 'primary' : 'ghost'}
                  size="sm"
                  onClick={() => handlePageChange(pageNum)}
                >
                  {pageNum}
                </Button>
              );
            })}
            <Button
              variant="secondary"
              size="sm"
              disabled={currentPage >= totalPages}
              onClick={() => handlePageChange(currentPage + 1)}
            >
              Próxima
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}
