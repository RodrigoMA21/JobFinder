import { useQuery } from '@tanstack/react-query';
import { fetchFilterOptions, fetchJobById, fetchJobs, type JobSearchParams } from '../services/api';

export function useJobs(params: JobSearchParams) {
  return useQuery({
    queryKey: ['jobs', params],
    queryFn: () => fetchJobs(params),
    staleTime: 1000 * 60 * 2,
    placeholderData: (prev) => prev,
  });
}

export function useJob(id: string) {
  return useQuery({
    queryKey: ['job', id],
    queryFn: () => fetchJobById(id),
    enabled: !!id,
    staleTime: 1000 * 60 * 5,
  });
}

export function useFilterOptions() {
  return useQuery({
    queryKey: ['filter-options'],
    queryFn: fetchFilterOptions,
    staleTime: 1000 * 60 * 10,
  });
}
