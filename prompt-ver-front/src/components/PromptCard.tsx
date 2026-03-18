import { GitBranch, GitCompare, Eye } from 'lucide-react';
import type { PromptResponse } from '../types';

interface Props {
  prompt: PromptResponse;
  onTimeline: (prompt: PromptResponse) => void;
  onCompare: (prompt: PromptResponse) => void;
  onDetails: (prompt: PromptResponse) => void;
}

export function PromptCard({ prompt, onTimeline, onCompare, onDetails }: Props) {
  const preview = prompt.content
    ? prompt.content.length > 120
      ? prompt.content.slice(0, 120) + '...'
      : prompt.content
    : null;

  return (
    <div className="group relative bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl p-5 shadow-sm hover:shadow-md hover:border-blue-300 dark:hover:border-blue-700 transition-all duration-200">
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-gray-900 dark:text-gray-100 text-base truncate">
            {prompt.name}
          </h3>
          <div className="mt-1 flex items-center gap-2">
            {prompt.active_version_id ? (
              <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 inline-block" />
                Versão ativa
              </span>
            ) : (
              <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400 border border-gray-200 dark:border-gray-700">
                Sem versão ativa
              </span>
            )}
          </div>
        </div>
        <div className="flex items-center gap-1 shrink-0">
          <ActionButton
            icon={<GitBranch className="w-4 h-4" />}
            label="Timeline"
            onClick={() => onTimeline(prompt)}
          />
          <ActionButton
            icon={<GitCompare className="w-4 h-4" />}
            label="Comparar"
            onClick={() => onCompare(prompt)}
          />
          <ActionButton
            icon={<Eye className="w-4 h-4" />}
            label="Detalhes"
            onClick={() => onDetails(prompt)}
            highlight
          />
        </div>
      </div>

      {preview && (
        <p className="mt-3 text-sm text-gray-500 dark:text-gray-400 leading-relaxed font-mono bg-gray-50 dark:bg-gray-800/60 rounded-lg px-3 py-2 border border-gray-100 dark:border-gray-800">
          {preview}
        </p>
      )}

      <div className="mt-3 pt-3 border-t border-gray-100 dark:border-gray-800 flex items-center justify-between">
        <span className="text-xs text-gray-400 dark:text-gray-500">
          Atualizado {new Date(prompt.updated_at).toLocaleDateString('pt-BR')}
        </span>
        <span
          className={`text-xs font-medium px-2 py-0.5 rounded-full ${
            prompt.status === 'active'
              ? 'text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/20'
              : 'text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-gray-800'
          }`}
        >
          {prompt.status}
        </span>
      </div>
    </div>
  );
}

interface ActionButtonProps {
  icon: React.ReactNode;
  label: string;
  onClick: () => void;
  highlight?: boolean;
}

function ActionButton({ icon, label, onClick, highlight }: ActionButtonProps) {
  return (
    <button
      onClick={onClick}
      title={label}
      className={`p-2 rounded-lg transition-all duration-150 ${
        highlight
          ? 'text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/30'
          : 'text-gray-400 dark:text-gray-500 hover:text-gray-700 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
      }`}
    >
      {icon}
    </button>
  );
}
