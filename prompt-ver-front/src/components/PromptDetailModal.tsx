import { useState, useEffect } from 'react';
import { X, Copy, Check, Pencil, Save, XCircle, Tag, Clock, Layers } from 'lucide-react';
import type { PromptResponse, PromptDetailResponse } from '../types';
import { promptsService } from '../services/api';

interface Props {
  prompt: PromptResponse | null;
  onClose: () => void;
  onSuccess: (message: string) => void;
  onError: (message: string) => void;
  onUpdated: () => void;
}

export function PromptDetailModal({ prompt, onClose, onSuccess, onError, onUpdated }: Props) {
  const [detail, setDetail] = useState<PromptDetailResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [editing, setEditing] = useState(false);
  const [editContent, setEditContent] = useState('');
  const [saving, setSaving] = useState(false);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    if (!prompt) return;
    setDetail(null);
    setEditing(false);
    setLoading(true);
    promptsService
      .getById(prompt.id)
      .then((d) => {
        setDetail(d);
        const active = d.versions.find((v) => v.is_active);
        setEditContent(active?.content ?? '');
      })
      .catch(() => onError('Erro ao carregar detalhes do prompt.'))
      .finally(() => setLoading(false));
  }, [prompt]);

  if (!prompt) return null;

  const activeVersion = detail?.versions.find((v) => v.is_active);
  const activeContent = activeVersion?.content ?? prompt.content ?? '';

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(activeContent);
      setCopied(true);
      onSuccess('Conteúdo copiado para a área de transferência!');
      setTimeout(() => setCopied(false), 2000);
    } catch {
      onError('Não foi possível copiar o conteúdo.');
    }
  };

  const handleSave = async () => {
    if (!editContent.trim()) {
      onError('O conteúdo não pode ser vazio.');
      return;
    }
    setSaving(true);
    try {
      await promptsService.updateContent(prompt.id, { content: editContent });
      onSuccess('Nova versão criada com sucesso!');
      setEditing(false);
      onUpdated();
      const updated = await promptsService.getById(prompt.id);
      setDetail(updated);
    } catch {
      onError('Erro ao salvar nova versão.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 z-40 flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" onClick={onClose} />
      <div className="relative z-10 w-full max-w-2xl bg-white dark:bg-gray-900 rounded-2xl shadow-2xl border border-gray-200 dark:border-gray-800 flex flex-col max-h-[90vh]">
        <div className="flex items-center justify-between p-5 border-b border-gray-100 dark:border-gray-800">
          <div className="flex-1 min-w-0">
            <h2 className="text-lg font-bold text-gray-900 dark:text-gray-100 truncate">
              {prompt.name}
            </h2>
            <div className="flex items-center gap-3 mt-1">
              {activeVersion && (
                <span className="flex items-center gap-1 text-xs text-gray-500 dark:text-gray-400">
                  <Layers className="w-3 h-3" />
                  v{activeVersion.version_number}
                </span>
              )}
              <span className="flex items-center gap-1 text-xs text-gray-500 dark:text-gray-400">
                <Clock className="w-3 h-3" />
                {new Date(prompt.updated_at).toLocaleString('pt-BR')}
              </span>
              <span className="flex items-center gap-1 text-xs">
                <Tag className="w-3 h-3 text-blue-500" />
                <span className="text-blue-600 dark:text-blue-400 font-medium">{prompt.status}</span>
              </span>
            </div>
          </div>
          <button
            onClick={onClose}
            className="ml-3 p-2 rounded-lg text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-5">
          {loading ? (
            <div className="flex items-center justify-center py-12">
              <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
            </div>
          ) : (
            <>
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-semibold text-gray-700 dark:text-gray-300">
                  Conteúdo da versão ativa
                </span>
                <div className="flex items-center gap-2">
                  {!editing ? (
                    <>
                      <button
                        onClick={handleCopy}
                        className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-lg border border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                      >
                        {copied ? <Check className="w-3.5 h-3.5 text-emerald-500" /> : <Copy className="w-3.5 h-3.5" />}
                        {copied ? 'Copiado!' : 'Copiar'}
                      </button>
                      <button
                        onClick={() => {
                          setEditContent(activeContent);
                          setEditing(true);
                        }}
                        className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-lg bg-blue-600 hover:bg-blue-700 text-white transition-colors"
                      >
                        <Pencil className="w-3.5 h-3.5" />
                        Editar
                      </button>
                    </>
                  ) : (
                    <>
                      <button
                        onClick={() => setEditing(false)}
                        className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-lg border border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                      >
                        <XCircle className="w-3.5 h-3.5" />
                        Cancelar
                      </button>
                      <button
                        onClick={handleSave}
                        disabled={saving}
                        className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white transition-colors disabled:opacity-60"
                      >
                        {saving ? (
                          <div className="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                        ) : (
                          <Save className="w-3.5 h-3.5" />
                        )}
                        {saving ? 'Salvando...' : 'Salvar nova versão'}
                      </button>
                    </>
                  )}
                </div>
              </div>

              {editing ? (
                <textarea
                  value={editContent}
                  onChange={(e) => setEditContent(e.target.value)}
                  className="w-full h-64 p-4 text-sm font-mono bg-gray-50 dark:bg-gray-800 border border-blue-400 dark:border-blue-600 rounded-xl text-gray-800 dark:text-gray-200 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500/40 transition-all"
                />
              ) : (
                <div className="p-4 bg-gray-50 dark:bg-gray-800/60 border border-gray-100 dark:border-gray-700 rounded-xl">
                  <pre className="text-sm text-gray-700 dark:text-gray-300 font-mono whitespace-pre-wrap leading-relaxed">
                    {activeContent || <span className="text-gray-400 italic">Sem conteúdo disponível.</span>}
                  </pre>
                </div>
              )}

              {detail && detail.versions.length > 0 && (
                <div className="mt-5">
                  <h3 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                    Histórico de versões ({detail.versions.length})
                  </h3>
                  <div className="space-y-2">
                    {[...detail.versions].reverse().map((v) => (
                      <div
                        key={v.id}
                        className={`flex items-center justify-between px-3 py-2 rounded-lg border text-sm ${
                          v.is_active
                            ? 'border-emerald-300 dark:border-emerald-700 bg-emerald-50 dark:bg-emerald-900/20'
                            : 'border-gray-100 dark:border-gray-800 bg-white dark:bg-gray-900'
                        }`}
                      >
                        <div className="flex items-center gap-2">
                          <span className="font-medium text-gray-700 dark:text-gray-300">
                            v{v.version_number}
                          </span>
                          {v.is_active && (
                            <span className="text-xs font-medium text-emerald-600 dark:text-emerald-400">
                              ativa
                            </span>
                          )}
                        </div>
                        <span className="text-xs text-gray-400 dark:text-gray-500">
                          {new Date(v.created_at).toLocaleString('pt-BR')}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
