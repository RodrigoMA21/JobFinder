import { Input } from '../ui/Input';
import { Select } from '../ui/Select';
import { Combobox } from '../ui/Combobox';
import { Button } from '../ui/Button';
import { useFilterOptions } from '../../hooks/useJobs';
import type { JobSearchParams } from '../../services/api';

interface FilterBarProps {
  params: JobSearchParams;
  onChange: (params: JobSearchParams) => void;
  onReset: () => void;
}

const modalityOptions = [
  { value: 'remote', label: 'Remoto' },
  { value: 'hybrid', label: 'Híbrido' },
  { value: 'onsite', label: 'Presencial' },
];

const contractOptions = [
  { value: 'clt', label: 'CLT' },
  { value: 'pj', label: 'PJ' },
  { value: 'freelancer', label: 'Freelancer' },
  { value: 'internship', label: 'Estágio' },
];

const levelOptions = [
  { value: 'internship', label: 'Estágio' },
  { value: 'junior', label: 'Júnior' },
  { value: 'mid', label: 'Pleno' },
  { value: 'senior', label: 'Sênior' },
];

const sortOptions = [
  { value: 'published_at', label: 'Mais recentes' },
  { value: 'salary_min', label: 'Maior salário' },
  { value: 'salary_max', label: 'Menor salário' },
];

export function FilterBar({ params, onChange, onReset }: FilterBarProps) {
  const { data: filterOptions } = useFilterOptions();
  const cities = filterOptions?.cities ?? [];

  const update = (key: keyof JobSearchParams, value: string | number | undefined) => {
    onChange({ ...params, [key]: value || undefined, page: 1 });
  };

  return (
    <div className="space-y-4 rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-4 sm:p-6">
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Input
          placeholder="Cargo, tecnologia ou empresa..."
          value={params.title || ''}
          onChange={(e) => update('title', e.target.value)}
        />
        <Combobox
          options={cities}
          value={params.city || ''}
          onChange={(v) => update('city', v)}
          placeholder="Cidade"
        />
        <Select
          placeholder="Modalidade"
          options={modalityOptions}
          value={params.modality || ''}
          onChange={(e) => update('modality', e.target.value)}
        />
        <Select
          placeholder="Tipo de contrato"
          options={contractOptions}
          value={params.contract_type || ''}
          onChange={(e) => update('contract_type', e.target.value)}
        />
        <Select
          placeholder="Nível"
          options={levelOptions}
          value={params.level || ''}
          onChange={(e) => update('level', e.target.value)}
        />
        <Select
          placeholder="Ordenar por"
          options={sortOptions}
          value={params.sort_by || 'published_at'}
          onChange={(e) => update('sort_by', e.target.value)}
        />
        <div className="flex items-end gap-2 sm:col-span-2 lg:col-span-2">
          <Input
            type="number"
            placeholder="Salário mínimo"
            value={params.salary_min || ''}
            onChange={(e) => update('salary_min', e.target.value ? Number(e.target.value) : undefined)}
          />
          <Input
            type="number"
            placeholder="Salário máximo"
            value={params.salary_max || ''}
            onChange={(e) => update('salary_max', e.target.value ? Number(e.target.value) : undefined)}
          />
        </div>
      </div>
      <div className="flex justify-end">
        <Button variant="ghost" size="sm" onClick={onReset}>
          Limpar filtros
        </Button>
      </div>
    </div>
  );
}
