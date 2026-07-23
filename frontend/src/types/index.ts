export interface Company {
  id: string;
  name: string;
  logo_url: string | null;
  website: string | null;
}

export interface Technology {
  id: string;
  name: string;
}

export type Modality = 'remote' | 'hybrid' | 'onsite';
export type ContractType = 'clt' | 'pj' | 'freelancer' | 'internship';
export type Level = 'internship' | 'junior' | 'mid' | 'senior';

export interface JobSummary {
  id: string;
  title: string;
  company: Company;
  city: string | null;
  state: string | null;
  modality: Modality;
  contract_type: ContractType;
  level: Level;
  salary_min: number | null;
  salary_max: number | null;
  currency: string;
  technologies: Technology[];
  published_at: string | null;
  application_url: string | null;
}

export interface JobDetail extends JobSummary {
  description: string;
  requirements: string | null;
  benefits: string | null;
  source: string;
  created_at: string;
  updated_at: string;
}

export interface PaginationMeta {
  page: number;
  per_page: number;
  total: number;
  total_pages: number;
}

export interface PaginatedResponse<T> {
  success: boolean;
  data: T[];
  meta: PaginationMeta;
  error: null | Record<string, unknown>;
}

export interface SingleResponse<T> {
  success: boolean;
  data: T;
  error: null | Record<string, unknown>;
}

export interface FilterOptions {
  modalities: Modality[];
  contract_types: ContractType[];
  levels: Level[];
  cities: string[];
  states: string[];
  technologies: string[];
}
