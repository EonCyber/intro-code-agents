import { useState, useEffect } from 'react';
import { X, GitBranch, AlertCircle, Clock } from 'lucide-react';
import { promptsService } from '../../services/api';
import type { PromptResponse, PromptVersionResponse } from '../../types';
import { VersionNode } from './VersionNode';

interface Props {
  prompt: PromptResponse | null;
  onClose: () => void;
  onCompareVersion: (prompt: PromptResponse, version: PromptVersionResponse) => void;
  onError: (msg: string) => void;
}

export function TimelineModal({ prompt, onClose, onCompareVersion, onError }: Props) {
  const [versions, setVersions] = useState<PromptVersionResponse[]>([]);
  const [loading, setLoading] = useState(false);
  const [fetchError, setFetchError] = useState<string | null>(null);

  useEffect(() => {
    if (!prompt) return;
    setVersions([]);
    setFetchError(null);
    load(prompt.id);
  }, [prompt]);

  const load = async (promptId: string) => {
    setLoading(true);
    try {
      const data = await promptsService.listVersions(promptId);
      const sorted = [...data].sort((a, b) => b.version_number - a.version_number);
      setVersions(sorted);
    } catch {
      setFetchError('Não foi possível carregar o histórico de versões.');
      onError('Não foi possível carregar o histórico de versões.');
    } finally {
      setLoading(false);
    }
  };

  if (!prompt) return null;

  return (
    <div className="fixed inset-0 z-40 flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={onClose} />

      <div className="relative z-10 w-full max-w-2xl max-h-[88vh] flex flex-col bg-white dark:bg-gray-900 rounded-2xl shadow-2xl border border-gray-200 dark:border-gray-800 overflow-hidden">
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-100 dark:border-gray-800 shrink-0">
          <div className="flex items-center gap-2.5 min-w-0">
            <div className="w-7 h-7 rounded-lg bg-blue-600/10 dark:bg-blue-500/10 flex items-center justify-center shrink-0">
              <GitBranch className="w-3.5 h-3.5 text-blue-600 dark:text-blue-400" />
            </div>
            <div className="min-w-0">
              <h2 className="text-base font-bold text-gray-900 dark:text-gray-100 leading-tight truncate">
                Histórico de versões
              </h2>
              <p className="text-xs text-gray-500 dark:text-gray-400 truncate">{prompt.name}</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-lg text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors shrink-0"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {!loading && !fetchError && versions.length > 0 && (
          <div className="px-6 py-2 border-b border-gray-100 dark:border-gray-800 shrink-0 flex items-center justify-between">
            <div className="flex items-center gap-1.5 text-xs text-gray-500 dark:text-gray-400">
              <Clock className="w-3.5 h-3.5" />
              <span>{versions.length} versão{versions.length !== 1 ? 'ões' : ''} no histórico</span>
            </div>
            <span className="text-xs text-gray-400 dark:text-gray-500">mais recente primeiro</span>
          </div>
        )}

        <div className="flex-1 overflow-y-auto px-6 py-4">
          {loading && (
            <div className="flex flex-col items-center justify-center py-20 gap-3">
              <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
              <p className="text-sm text-gray-500 dark:text-gray-400">Carregando histórico...</p>
            </div>
          )}

          {!loading && fetchError && (
            <div className="flex flex-col items-center justify-center py-16 gap-4">
              <div className="w-10 h-10 rounded-2xl bg-red-100 dark:bg-red-900/20 flex items-center justify-center">
                <AlertCircle className="w-5 h-5 text-red-500" />
              </div>
              <div className="text-center">
                <p className="text-sm font-semibold text-gray-700 dark:text-gray-300">{fetchError}</p>
                <button
                  onClick={() => load(prompt.id)}
                  className="mt-2 text-sm text-blue-600 dark:text-blue-400 hover:underline font-medium"
                >
                  Tentar novamente
                </button>
              </div>
            </div>
          )}

          {!loading && !fetchError && versions.length === 0 && (
            <div className="flex flex-col items-center justify-center py-16 gap-3 text-center">
              <div className="w-12 h-12 rounded-2xl bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
                <GitBranch className="w-6 h-6 text-gray-400 dark:text-gray-500" />
              </div>
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Nenhuma versão encontrada</p>
              <p className="text-xs text-gray-400 dark:text-gray-500">Crie uma versão para começar o histórico.</p>
            </div>
          )}

          {!loading && !fetchError && versions.length > 0 && (
            <div>
              {versions.map((version, idx) => (
                <VersionNode
                  key={version.id}
                  version={version}
                  isFirst={idx === 0}
                  isLast={idx === versions.length - 1}
                  onCompare={(v) => onCompareVersion(prompt, v)}
                />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
