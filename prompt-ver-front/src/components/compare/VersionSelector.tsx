import type { PromptVersionResponse } from '../../types';

interface Props {
  versions: PromptVersionResponse[];
  beforeId: string;
  afterId: string;
  onBeforeChange: (id: string) => void;
  onAfterChange: (id: string) => void;
  disabled?: boolean;
}

export function VersionSelector({ versions, beforeId, afterId, onBeforeChange, onAfterChange, disabled }: Props) {
  return (
    <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
      <VersionSelect
        label="Base"
        value={beforeId}
        versions={versions}
        onChange={onBeforeChange}
        disabled={disabled}
        colorClass="border-red-300 dark:border-red-700 focus:ring-red-400/40 focus:border-red-500"
        badgeClass="bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400"
      />

      <div className="flex items-center justify-center text-gray-400 dark:text-gray-500 shrink-0 font-mono text-sm">
        →
      </div>

      <VersionSelect
        label="Comparada"
        value={afterId}
        versions={versions}
        onChange={onAfterChange}
        disabled={disabled}
        colorClass="border-emerald-300 dark:border-emerald-700 focus:ring-emerald-400/40 focus:border-emerald-500"
        badgeClass="bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400"
      />
    </div>
  );
}

interface SelectProps {
  label: string;
  value: string;
  versions: PromptVersionResponse[];
  onChange: (id: string) => void;
  disabled?: boolean;
  colorClass: string;
  badgeClass: string;
}

function VersionSelect({ label, value, versions, onChange, disabled, colorClass, badgeClass }: SelectProps) {
  return (
    <div className="flex-1 min-w-0">
      <label className="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1.5">
        Versão {label}
      </label>
      <div className="relative">
        <select
          value={value}
          onChange={(e) => onChange(e.target.value)}
          disabled={disabled}
          className={`w-full appearance-none pl-3 pr-8 py-2 text-sm rounded-xl border bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed ${colorClass}`}
        >
          {versions.map((v) => (
            <option key={v.id} value={v.id}>
              v{v.version_number} — {new Date(v.created_at).toLocaleDateString('pt-BR', { day: '2-digit', month: 'short', year: 'numeric' })}
              {v.is_active ? ' (ativa)' : ''}
            </option>
          ))}
        </select>
        <div className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-gray-400">
          <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </div>
      {value && (
        <div className="mt-1">
          {(() => {
            const v = versions.find((x) => x.id === value);
            return v ? (
              <span className={`inline-block text-xs px-2 py-0.5 rounded-full font-medium ${badgeClass}`}>
                v{v.version_number}{v.is_active ? ' · ativa' : ''}
              </span>
            ) : null;
          })()}
        </div>
      )}
    </div>
  );
}
