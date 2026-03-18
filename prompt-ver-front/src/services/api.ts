import axios from 'axios';
import type {
  PromptResponse,
  PromptDetailResponse,
  PromptVersionResponse,
  VersionDiffResponse,
  CreatePromptRequest,
  AddVersionBody,
  UpdateContentBody,
  ActivateVersionBody,
  CompareVersionsBody,
} from '../types';
import { MOCK_VERSIONS } from '../mocks/data';
import { computeDiff } from '../utils/diff';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const promptsService = {
  listActive: async (): Promise<PromptResponse[]> => {
    const { data } = await apiClient.get<PromptResponse[]>('/prompts/active');
    return data;
  },

  listDeleted: async (): Promise<PromptResponse[]> => {
    const { data } = await apiClient.get<PromptResponse[]>('/prompts/deleted');
    return data;
  },

  getById: async (promptId: string): Promise<PromptDetailResponse> => {
    const { data } = await apiClient.get<PromptDetailResponse>(`/prompts/${promptId}`);
    return data;
  },

  create: async (payload: CreatePromptRequest): Promise<PromptResponse> => {
    const { data } = await apiClient.post<PromptResponse>('/prompts/', payload);
    return data;
  },

  softDelete: async (promptId: string): Promise<PromptResponse> => {
    const { data } = await apiClient.delete<PromptResponse>(`/prompts/${promptId}`);
    return data;
  },

  recover: async (promptId: string): Promise<PromptResponse> => {
    const { data } = await apiClient.post<PromptResponse>(`/prompts/${promptId}/recover`);
    return data;
  },

  updateContent: async (promptId: string, payload: UpdateContentBody): Promise<PromptVersionResponse> => {
    const { data } = await apiClient.put<PromptVersionResponse>(`/prompts/${promptId}/content`, payload);
    return data;
  },

  listVersions: async (promptId: string): Promise<PromptVersionResponse[]> => {
    if (MOCK_VERSIONS[promptId]) {
      return MOCK_VERSIONS[promptId];
    }
    const { data } = await apiClient.get<PromptVersionResponse[]>(`/prompts/${promptId}/versions`);
    return data;
  },

  addVersion: async (promptId: string, payload: AddVersionBody): Promise<PromptVersionResponse> => {
    const { data } = await apiClient.post<PromptVersionResponse>(`/prompts/${promptId}/versions`, payload);
    return data;
  },

  activateVersion: async (promptId: string, payload: ActivateVersionBody): Promise<PromptResponse> => {
    const { data } = await apiClient.post<PromptResponse>(`/prompts/${promptId}/activate`, payload);
    return data;
  },

  compareVersions: async (promptId: string, payload: CompareVersionsBody): Promise<VersionDiffResponse> => {
    const mockVersions = MOCK_VERSIONS[promptId];
    if (mockVersions) {
      const before = mockVersions.find((v) => v.id === payload.version_id_before);
      const after = mockVersions.find((v) => v.id === payload.version_id_after);
      if (before && after) {
        return computeDiff(
          promptId,
          before.id,
          after.id,
          before.version_number,
          after.version_number,
          before.content,
          after.content
        );
      }
    }
    const { data } = await apiClient.post<VersionDiffResponse>(`/prompts/${promptId}/compare`, payload);
    return data;
  },
};
