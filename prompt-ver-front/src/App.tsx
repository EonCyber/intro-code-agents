import { useState, useEffect, useMemo } from 'react';
import { Sun, Moon, Search, RefreshCw, Terminal, AlertCircle } from 'lucide-react';
import { useTheme } from './hooks/useTheme';
import { useToast } from './hooks/useToast';
import { promptsService } from './services/api';
import type { PromptResponse } from './types';
import { PromptCard } from './components/PromptCard';
import { PromptDetailModal } from './components/PromptDetailModal';
import { CreatePromptModal } from './components/CreatePromptModal';
import { CompareModal } from './components/compare/CompareModal';
import { TimelineModal } from './components/timeline/TimelineModal';
import { ToastContainer } from './components/ToastContainer';
import { GeometricBackground } from './components/GeometricBackground';

export default function App() {
  const { isDark, toggle } = useTheme();
  const { toasts, addToast, removeToast } = useToast();

  const [prompts, setPrompts] = useState<PromptResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState('');
  const [selectedPrompt, setSelectedPrompt] = useState<PromptResponse | null>(null);
  const [comparePrompt, setComparePrompt] = useState<PromptResponse | null>(null);
  const [timelinePrompt, setTimelinePrompt] = useState<PromptResponse | null>(null);
  const [showCreate, setShowCreate] = useState(false);

  const MOCK_PROMPTS: PromptResponse[] = [
    {
      id: 'mock-1',
      name: 'Assistente de Código',
      status: 'active',
      active_version_id: 'v1',
      created_at: '2025-03-10T10:00:00Z',
      updated_at: '2025-03-14T14:30:00Z',
      content:
        'Você é um assistente especializado em desenvolvimento de software. Responda sempre com exemplos práticos de código, explique o raciocínio por trás de cada decisão técnica e sugira boas práticas de acordo com o contexto.',
    },
    {
      id: 'mock-2',
      name: 'Resumidor de Documentos',
      status: 'active',
      active_version_id: 'v2',
      created_at: '2025-03-12T09:00:00Z',
      updated_at: '2025-03-15T11:00:00Z',
      content:
        'Resuma o documento fornecido de forma clara e objetiva. Identifique os pontos principais, mantenha a essência do conteúdo original e organize o resumo em tópicos quando apropriado.',
    },
  ];

  const fetchPrompts = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await promptsService.listActive();
      setPrompts(data);
    } catch {
      setPrompts(MOCK_PROMPTS);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPrompts();
  }, []);

  const filtered = useMemo(
    () =>
      prompts.filter((p) =>
        p.name.toLowerCase().includes(search.toLowerCase())
      ),
    [prompts, search]
  );

  const handleCreated = (prompt: PromptResponse) => {
    setPrompts((prev) => [prompt, ...prev]);
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950 transition-colors duration-200">
      <GeometricBackground />

      <header className="sticky top-0 z-30 bg-white/80 dark:bg-gray-950/80 backdrop-blur-md border-b border-gray-200 dark:border-gray-800">
        <div className="max-w-3xl mx-auto px-4 h-16 flex items-center justify-between gap-4">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center">
              <Terminal className="w-4 h-4 text-white" />
            </div>
            <div>
              <h1 className="text-base font-bold text-gray-900 dark:text-gray-100 leading-tight">
                Prompt Manager
              </h1>
              <p className="text-xs text-gray-500 dark:text-gray-400 leading-tight hidden sm:block">
                Gerencie seus prompts e versões
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={fetchPrompts}
              disabled={loading}
              title="Recarregar"
              className="p-2 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors disabled:opacity-50"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            </button>
            <button
              onClick={toggle}
              title={isDark ? 'Modo claro' : 'Modo escuro'}
              className="p-2 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
            >
              {isDark ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-3xl mx-auto px-4 py-8">
        <div className="mb-6">
          <div className="relative">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 dark:text-gray-500" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Buscar prompts pelo nome..."
              className="w-full pl-10 pr-4 py-2.5 text-sm rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-blue-500 transition-all shadow-sm"
            />
          </div>
          {!loading && !error && (
            <p className="mt-2 text-xs text-gray-500 dark:text-gray-400 text-center">
              {filtered.length} prompt{filtered.length !== 1 ? 's' : ''} encontrado{filtered.length !== 1 ? 's' : ''}
            </p>
          )}
        </div>

        {loading && (
          <div className="flex flex-col items-center justify-center py-20 gap-3">
            <div className="w-10 h-10 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
            <p className="text-sm text-gray-500 dark:text-gray-400">Carregando prompts...</p>
          </div>
        )}

        {!loading && error && (
          <div className="flex flex-col items-center justify-center py-16 gap-4">
            <div className="w-12 h-12 rounded-2xl bg-red-100 dark:bg-red-900/20 flex items-center justify-center">
              <AlertCircle className="w-6 h-6 text-red-500" />
            </div>
            <div className="text-center">
              <p className="text-sm font-semibold text-gray-700 dark:text-gray-300">{error}</p>
              <button
                onClick={fetchPrompts}
                className="mt-3 text-sm text-blue-600 dark:text-blue-400 hover:underline font-medium"
              >
                Tentar novamente
              </button>
            </div>
          </div>
        )}

        {!loading && !error && filtered.length === 0 && (
          <div className="flex flex-col items-center justify-center py-20 gap-3">
            <div className="w-14 h-14 rounded-2xl bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
              <Terminal className="w-7 h-7 text-gray-400 dark:text-gray-500" />
            </div>
            <div className="text-center">
              <p className="text-base font-semibold text-gray-700 dark:text-gray-300">
                {search ? 'Nenhum resultado encontrado' : 'Nenhum prompt criado ainda'}
              </p>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                {search
                  ? 'Tente buscar por outro nome'
                  : 'Clique no botão "+" para criar seu primeiro prompt'}
              </p>
            </div>
          </div>
        )}

        {!loading && !error && filtered.length > 0 && (
          <div className="space-y-3 animate-fade-in">
            {filtered.map((prompt) => (
              <PromptCard
                key={prompt.id}
                prompt={prompt}
                onTimeline={(p) => setTimelinePrompt(p)}
                onCompare={(p) => setComparePrompt(p)}
                onDetails={(p) => setSelectedPrompt(p)}
              />
            ))}
          </div>
        )}
      </main>

      <button
        onClick={() => setShowCreate(true)}
        title="Criar novo prompt"
        className="fixed bottom-6 right-6 w-14 h-14 rounded-full bg-blue-600 hover:bg-blue-700 text-white shadow-lg hover:shadow-xl transition-all duration-200 flex items-center justify-center text-2xl font-light z-30 hover:scale-105 active:scale-95"
      >
        +
      </button>

      <PromptDetailModal
        prompt={selectedPrompt}
        onClose={() => setSelectedPrompt(null)}
        onSuccess={(msg) => addToast(msg, 'success')}
        onError={(msg) => addToast(msg, 'error')}
        onUpdated={fetchPrompts}
      />

      <CreatePromptModal
        isOpen={showCreate}
        onClose={() => setShowCreate(false)}
        onSuccess={(msg) => addToast(msg, 'success')}
        onError={(msg) => addToast(msg, 'error')}
        onCreated={handleCreated}
      />

      <TimelineModal
        prompt={timelinePrompt}
        onClose={() => setTimelinePrompt(null)}
        onCompareVersion={(p) => {
          setTimelinePrompt(null);
          setComparePrompt(p);
        }}
        onError={(msg) => addToast(msg, 'error')}
      />

      <CompareModal
        prompt={comparePrompt}
        onClose={() => setComparePrompt(null)}
        onError={(msg) => addToast(msg, 'error')}
      />

      <ToastContainer toasts={toasts} onRemove={removeToast} />
    </div>
  );
}
