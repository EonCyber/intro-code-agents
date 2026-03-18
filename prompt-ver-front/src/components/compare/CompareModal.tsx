import { useState, useEffect } from 'react';
import { X, GitCompare, AlertCircle, ArrowRight } from 'lucide-react';
import { promptsService } from '../../services/api';
import type { PromptResponse, PromptVersionResponse, VersionDiffResponse } from '../../types';
import { VersionSelector } from './VersionSelector';
import { DiffViewer } from './DiffViewer';

interface Props {
  prompt: PromptResponse | null;
  onClose: () => void;
  onError: (msg: string) => void;
}

export function CompareModal({ prompt, onClose, onError }: Props) {
  const [versions, setVersions] = useState<PromptVersionResponse[]>([]);
  const [loadingVersions, setLoadingVersions] = useState(false);
  const [beforeId, setBeforeId] = useState('');
  const [afterId, setAfterId] = useState('');
  const [diff, setDiff] = useState<VersionDiffResponse | null>(null);
  const [loadingDiff, setLoadingDiff] = useState(false);
  const [diffError, setDiffError] = useState<string | null>(null);

  useEffect(() => {
    if (!prompt) return;
    setVersions([]);
    setBeforeId('');
    setAfterId('');
    setDiff(null);
    setDiffError(null);
    loadVersions(prompt.id);
  }, [prompt]);

  const loadVersions = async (promptId: string) => {
    setLoadingVersions(true);
    try {
      const data = await promptsService.listVersions(promptId);
      setVersions(data);
      if (data.length >= 2) {
        setBeforeId(data[0].id);
        setAfterId(data[data.length - 1].id);
      } else if (data.length === 1) {
        setBeforeId(data[0].id);
        setAfterId(data[0].id);
      }
    } catch {
      onError('Não foi possível carregar as versões.');
    } finally {
      setLoadingVersions(false);
    }
  };

  const handleCompare = async () => {
    if (!prompt || !beforeId || !afterId) return;
    if (beforeId === afterId) {
      setDiffError('Selecione versões diferentes para comparar.');
      return;
    }
    setLoadingDiff(true);
    setDiff(null);
    setDiffError(null);
    try {
      const result = await promptsService.compareVersions(prompt.id, {
        version_id_before: beforeId,
        version_id_after: afterId,
      });
      setDiff(result);
    } catch {
      setDiffError('Falha ao comparar versões. Tente novamente.');
    } finally {
      setLoadingDiff(false);
    }
  };

  if (!prompt) return null;

  const canCompare = versions.length >= 2 && beforeId && afterId && beforeId !== afterId;

  return (
    <div className="fixed inset-0 z-40 flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={onClose} />

      <div className="relative z-10 w-full max-w-4xl max-h-[90vh] flex flex-col bg-white dark:bg-gray-900 rounded-2xl shadow-2xl border border-gray-200 dark:border-gray-800 overflow-hidden">
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-100 dark:border-gray-800 shrink-0">
          <div className="flex items-center gap-2.5 min-w-0">
            <div className="w-7 h-7 rounded-lg bg-blue-600/10 dark:bg-blue-500/10 flex items-center justify-center shrink-0">
              <GitCompare className="w-3.5 h-3.5 text-blue-600 dark:text-blue-400" />
            </div>
            <div className="min-w-0">
              <h2 className="text-base font-bold text-gray-900 dark:text-gray-100 leading-tight truncate">
                Comparar versões
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

        <div className="px-6 py-4 border-b border-gray-100 dark:border-gray-800 shrink-0">
          {loadingVersions ? (
            <div className="flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400">
              <div className="w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
              Carregando versões...
            </div>
          ) : versions.length === 0 ? (
            <div className="flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400">
              <AlertCircle className="w-4 h-4" />
              Nenhuma versão encontrada para este prompt.
            </div>
          ) : versions.length === 1 ? (
            <div className="flex items-center gap-2 text-sm text-amber-600 dark:text-amber-400">
              <AlertCircle className="w-4 h-4" />
              Este prompt possui apenas uma versão. Crie outra versão para comparar.
            </div>
          ) : (
            <div className="flex flex-col sm:flex-row items-end gap-3">
              <div className="flex-1 min-w-0">
                <VersionSelector
                  versions={versions}
                  beforeId={beforeId}
                  afterId={afterId}
                  onBeforeChange={setBeforeId}
                  onAfterChange={setAfterId}
                  disabled={loadingDiff}
                />
              </div>
              <button
                onClick={handleCompare}
                disabled={!canCompare || loadingDiff}
                className="flex items-center gap-2 px-4 py-2 text-sm font-semibold rounded-xl bg-blue-600 hover:bg-blue-700 text-white transition-colors disabled:opacity-50 disabled:cursor-not-allowed shrink-0"
              >
                {loadingDiff ? (
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                ) : (
                  <ArrowRight className="w-4 h-4" />
                )}
                {loadingDiff ? 'Comparando...' : 'Comparar'}
              </button>
            </div>
          )}
        </div>

        <div className="flex-1 overflow-y-auto px-6 py-4">
          {diffError && (
            <div className="flex items-center gap-2 text-sm text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-900/20 rounded-xl px-4 py-3 border border-red-200 dark:border-red-800 mb-4">
              <AlertCircle className="w-4 h-4 shrink-0" />
              {diffError}
            </div>
          )}

          {!diff && !loadingDiff && !diffError && versions.length >= 2 && (
            <div className="flex flex-col items-center justify-center py-16 gap-3 text-center">
              <div className="w-12 h-12 rounded-2xl bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
                <GitCompare className="w-6 h-6 text-gray-400 dark:text-gray-500" />
              </div>
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                Selecione duas versões e clique em Comparar
              </p>
              <p className="text-xs text-gray-400 dark:text-gray-500">
                O diff será exibido aqui no estilo GitHub
              </p>
            </div>
          )}

          {loadingDiff && (
            <div className="flex flex-col items-center justify-center py-16 gap-3">
              <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
              <p className="text-sm text-gray-500 dark:text-gray-400">Calculando diferenças...</p>
            </div>
          )}

          {diff && !loadingDiff && <DiffViewer diff={diff} />}
        </div>
      </div>
    </div>
  );
}
