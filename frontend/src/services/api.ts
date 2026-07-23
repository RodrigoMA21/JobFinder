import axios from 'axios';
import type { FilterOptions, JobDetail, JobSummary, PaginatedResponse, SingleResponse } from '../types';

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' },
});

export interface JobSearchParams {
  title?: string;
  company?: string;
  technology?: string;
  city?: string;
  state?: string;
  modality?: string;
  contract_type?: string;
  level?: string;
  salary_min?: number;
  salary_max?: number;
  sort_by?: string;
  sort_order?: string;
  page?: number;
  per_page?: number;
}

export async function fetchJobs(params: JobSearchParams): Promise<PaginatedResponse<JobSummary>> {
  const clean = Object.fromEntries(
    Object.entries(params).filter(([_, v]) => v !== undefined && v !== '' && v !== null)
  );
  const { data } = await api.get<PaginatedResponse<JobSummary>>('/jobs', { params: clean });
  return data;
}

export async function fetchJobById(id: string): Promise<SingleResponse<JobDetail>> {
  const { data } = await api.get<SingleResponse<JobDetail>>(`/jobs/${id}`);
  return data;
}

export async function fetchFilterOptions(): Promise<FilterOptions> {
  const { data } = await api.get<{ success: boolean; data: FilterOptions }>('/jobs/filters');
  return data.data;
}

export async function triggerSync(): Promise<Record<string, unknown>> {
  const { data } = await api.post('/jobs/sync');
  return data;
}
