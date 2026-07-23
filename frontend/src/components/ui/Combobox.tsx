import { useState, useRef, useEffect, useMemo } from 'react';

interface ComboboxProps {
  options: string[];
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  label?: string;
  emptyMessage?: string;
  notFoundMessage?: string;
}

export function Combobox({
  options,
  value,
  onChange,
  placeholder = '',
  label,
  emptyMessage = 'Nenhuma cidade disponível',
  notFoundMessage = 'Nenhuma cidade encontrada',
}: ComboboxProps) {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState(value);
  const inputRef = useRef<HTMLInputElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  const filtered = useMemo(() => {
    if (!query) return options;
    const q = query.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
    return options.filter((opt) =>
      opt.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').includes(q)
    );
  }, [options, query]);

  const isValid = value === '' || options.some((opt) => opt === value);

  useEffect(() => {
    setQuery(value);
  }, [value]);

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setOpen(false);
        if (!isValid) {
          onChange('');
          setQuery('');
        }
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isValid, onChange]);

  function handleSelect(option: string) {
    onChange(option);
    setQuery(option);
    setOpen(false);
    inputRef.current?.blur();
  }

  function handleInputChange(e: React.ChangeEvent<HTMLInputElement>) {
    const v = e.target.value;
    setQuery(v);
    if (v !== value) {
      onChange('');
    }
    setOpen(true);
  }

  function handleFocus() {
    setOpen(true);
  }

  return (
    <div className="flex flex-col gap-1 relative" ref={containerRef}>
      {label && (
        <label className="text-sm font-medium text-[var(--color-text-secondary)]">
          {label}
        </label>
      )}
      <div className="relative">
        <input
          ref={inputRef}
          type="text"
          value={query}
          onChange={handleInputChange}
          onFocus={handleFocus}
          placeholder={placeholder}
          className={`w-full rounded-lg border px-3 py-2 text-sm bg-[var(--color-surface)] text-[var(--color-text)] placeholder:text-[var(--color-text-muted)] focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)] transition-colors ${
            !isValid && value
              ? 'border-red-400 focus:ring-red-400'
              : 'border-[var(--color-border)]'
          }`}
          autoComplete="off"
        />
        {value && (
          <button
            type="button"
            onClick={() => {
              onChange('');
              setQuery('');
              inputRef.current?.focus();
            }}
            className="absolute right-2 top-1/2 -translate-y-1/2 text-[var(--color-text-muted)] hover:text-[var(--color-text)] transition-colors"
          >
            <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        )}
      </div>
      {!isValid && value && (
        <p className="text-xs text-red-400">Selecione uma cidade válida da lista</p>
      )}
      {open && (
        <div className="absolute top-full mt-1 left-0 right-0 z-50 max-h-60 overflow-auto rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] shadow-lg">
          {options.length === 0 ? (
            <p className="p-3 text-sm text-[var(--color-text-muted)]">{emptyMessage}</p>
          ) : filtered.length === 0 ? (
            <p className="p-3 text-sm text-[var(--color-text-muted)]">{notFoundMessage}</p>
          ) : (
            <ul>
              {filtered.map((option) => (
                <li
                  key={option}
                  role="option"
                  aria-selected={option === value}
                  onClick={() => handleSelect(option)}
                  className={`cursor-pointer px-3 py-2 text-sm transition-colors hover:bg-[var(--color-primary-light)] hover:text-[var(--color-primary)] ${
                    option === value ? 'bg-[var(--color-primary-light)] text-[var(--color-primary)] font-medium' : 'text-[var(--color-text)]'
                  }`}
                >
                  {option}
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}
