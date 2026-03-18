import type { PromptVersionResponse } from '../types';

export const MOCK_VERSIONS: Record<string, PromptVersionResponse[]> = {
  'mock-1': [
    {
      id: 'mock-1-v1',
      prompt_id: 'mock-1',
      version_number: 1,
      content:
        'Você é um assistente de desenvolvimento de software.\nResponda com exemplos de código.\nExplique o raciocínio por trás de cada decisão técnica.\nSugira boas práticas de acordo com o contexto.',
      created_at: '2025-03-10T10:00:00Z',
      is_active: false,
    },
    {
      id: 'mock-1-v2',
      prompt_id: 'mock-1',
      version_number: 2,
      content:
        'Você é um assistente sênior especializado em desenvolvimento de software.\nResponda sempre com exemplos práticos de código.\nExplique o raciocínio por trás de cada decisão técnica.\nSugira boas práticas de acordo com o contexto.\nConsidere aspectos de performance e segurança.\nPrefira soluções simples e legíveis.',
      created_at: '2025-03-14T14:30:00Z',
      is_active: true,
    },
  ],
  'mock-2': [
    {
      id: 'mock-2-v1',
      prompt_id: 'mock-2',
      version_number: 1,
      content:
        'Resuma o documento fornecido de forma clara e objetiva.\nIdentifique os pontos principais.\nMantenha a essência do conteúdo original.\nOrganize o resumo em tópicos quando apropriado.',
      created_at: '2025-03-12T09:00:00Z',
      is_active: false,
    },
    {
      id: 'mock-2-v2',
      prompt_id: 'mock-2',
      version_number: 2,
      content:
        'Resuma o documento fornecido de forma clara, objetiva e estruturada.\nIdentifique os pontos principais e secundários.\nMantenha a essência do conteúdo original.\nOrganize o resumo em tópicos numerados.\nDestaque citações relevantes quando presentes.\nInclua uma conclusão ao final do resumo.',
      created_at: '2025-03-15T11:00:00Z',
      is_active: true,
    },
  ],
};
