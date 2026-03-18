export interface PromptResponse {
  id: string;
  name: string;
  status: string;
  active_version_id?: string | null;
  created_at: string;
  updated_at: string;
  content?: string | null;
}

export interface PromptVersionResponse {
  id: string;
  prompt_id: string;
  version_number: number;
  content: string;
  created_at: string;
  is_active: boolean;
}

export interface PromptDetailResponse {
  id: string;
  name: string;
  status: string;
  active_version_id?: string | null;
  created_at: string;
  updated_at: string;
  versions: PromptVersionResponse[];
}

export interface DiffLineResponse {
  kind: string;
  content: string;
  line_number_before?: number | null;
  line_number_after?: number | null;
}

export interface VersionDiffResponse {
  prompt_id: string;
  version_id_before: string;
  version_id_after: string;
  version_number_before: number;
  version_number_after: number;
  lines: DiffLineResponse[];
  has_changes: boolean;
}

export interface CreatePromptRequest {
  name: string;
  content: string;
}

export interface AddVersionBody {
  content: string;
}

export interface UpdateContentBody {
  content: string;
}

export interface ActivateVersionBody {
  version_id: string;
}

export interface CompareVersionsBody {
  version_id_before: string;
  version_id_after: string;
}

export type ToastType = 'success' | 'error' | 'info';

export interface Toast {
  id: string;
  type: ToastType;
  message: string;
}
