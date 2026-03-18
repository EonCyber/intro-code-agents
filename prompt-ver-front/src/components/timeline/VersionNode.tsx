import { GitCommitHorizontal, CheckCircle2, ChevronDown, ChevronUp, GitCompare } from 'lucide-react';
import { useState } from 'react';
import type { PromptVersionResponse } from '../../types';

interface Props {
  version: PromptVersionResponse;
  isFirst: boolean;
  isLast: boolean;
  onCompare: (version: PromptVersionResponse) => void;
}

export function VersionNode({ version, isFirst, isLast, onCompare }: Props) {
  const [expanded, setExpanded] = useState(false);

  const formattedDate = new Date(version.created_at).toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  });

  const formattedTime = new Date(version.created_at).toLocaleTimeString('pt-BR', {
    hour: '2-digit',
    minute: '2-digit',
  });

  const preview = version.content.length > 160 ? version.content.slice(0, 160) + '...' : version.content;

  return (
    <div className="flex gap-4 group">
      <div className="flex flex-col items-center shrink-0">
        <div
          className={`w-px flex-shrink-0 ${isFirst ? 'bg-transparent' : 'bg-gray-200 dark:bg-gray-700'}`}
          style={{ height: '20px' }}
        />
        <div className="relative flex items-center justify-center">
          {version.is_active ? (
            <div className="w-8 h-8 rounded-full bg-blue-600 dark:bg-blue-500 flex items-center justify-center shadow-md ring-4 ring-blue-100 dark:ring-blue-900/40">
              <CheckCircle2 className="w-4 h-4 text-white" />
            </div>
          ) : (
            <div className="w-8 h-8 rounded-full bg-white dark:bg-gray-900 border-2 border-gray-300 dark:border-gray-600 flex items-center justify-center group-hover:border-blue-400 dark:group-hover:border-blue-500 transition-colors">
              <GitCommitHorizontal className="w-4 h-4 text-gray-400 dark:text-gray-500 group-hover:text-blue-500 dark:group-hover:text-blue-400 transition-colors" />
            </div>
          )}
        </div>
        <div
          className={`w-px flex-1 min-h-[16px] ${isLast ? 'bg-transparent' : 'bg-gray-200 dark:bg-gray-700'}`}
        />
      </div>

      <div className="flex-1 min-w-0 pb-4">
        <div
          className={`rounded-2xl border transition-all duration-200 overflow-hidden ${
            version.is_active
              ? 'border-blue-200 dark:border-blue-800 bg-blue-50/60 dark:bg-blue-950/20 shadow-sm'
              : 'border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 hover:border-gray-300 dark:hover:border-gray-700 hover:shadow-sm'
          }`}
        >
          <div className="px-4 py-3 flex items-start justify-between gap-3">
            <div className="flex items-center gap-2.5 min-w-0 flex-1">
              <div className="flex items-center gap-2 min-w-0">
                <span
                  className={`text-xs font-mono font-bold shrink-0 px-1.5 py-0.5 rounded ${
                    version.is_active
                      ? 'bg-blue-100 dark:bg-blue-900/40 text-blue-700 dark:text-blue-300'
                      : 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400'
                  }`}
                >
                  v{version.version_number}
                </span>
                {version.is_active && (
                  <span className="inline-flex items-center gap-1 text-xs px-2 py-0.5 rounded-full font-medium bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400 border border-blue-200 dark:border-blue-800 shrink-0">
                    <span className="w-1.5 h-1.5 rounded-full bg-blue-500 inline-block animate-pulse" />
                    ativa
                  </span>
                )}
              </div>
              <div className="text-xs text-gray-400 dark:text-gray-500 font-mono shrink-0">
                {formattedDate} · {formattedTime}
              </div>
            </div>

            <div className="flex items-center gap-1 shrink-0">
              <button
                onClick={() => onCompare(version)}
                title="Comparar com outra versão"
                className="p-1.5 rounded-lg text-gray-400 dark:text-gray-500 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors"
              >
                <GitCompare className="w-3.5 h-3.5" />
              </button>
              <button
                onClick={() => setExpanded((e) => !e)}
                title={expanded ? 'Recolher' : 'Expandir'}
                className="p-1.5 rounded-lg text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
              >
                {expanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
              </button>
            </div>
          </div>

          <div className="px-4 pb-3">
            <p className="text-xs text-gray-500 dark:text-gray-400 font-mono leading-relaxed bg-gray-50 dark:bg-gray-800/60 rounded-lg px-3 py-2 border border-gray-100 dark:border-gray-800">
              {expanded ? version.content : preview}
            </p>
            {version.content.length > 160 && (
              <button
                onClick={() => setExpanded((e) => !e)}
                className="mt-1.5 text-xs text-blue-600 dark:text-blue-400 hover:underline font-medium"
              >
                {expanded ? 'Ver menos' : 'Ver mais'}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
