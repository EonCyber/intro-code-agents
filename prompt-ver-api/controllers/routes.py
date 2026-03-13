from fastapi import APIRouter, Depends, Request

from models.prompt_models import (
    ActivateVersionBody,
    ActivateVersionRequest,
    AddVersionBody,
    AddVersionRequest,
    CompareVersionsBody,
    CompareVersionsRequest,
    CreatePromptRequest,
    GetPromptByIdRequest,
    ListActivePromptsRequest,
    ListDeletedPromptsRequest,
    ListVersionsRequest,
    PromptDetailResponse,
    PromptResponse,
    PromptVersionResponse,
    RecoverPromptRequest,
    SoftDeletePromptRequest,
    UpdateContentBody,
    UpdateContentRequest,
    VersionDiffResponse,
)
from services.prompt_service import PromptService

router = APIRouter(prefix="/prompts", tags=["Prompts"])


def get_prompt_service(request: Request) -> PromptService:
    return request.app.state.prompt_service


@router.post("/", response_model=PromptResponse)
async def create_prompt(
    req: CreatePromptRequest,
    service: PromptService = Depends(get_prompt_service),
) -> PromptResponse:
    return await service.create_prompt(req)


@router.post("/{prompt_id}/versions", response_model=PromptVersionResponse)
async def add_version(
    prompt_id: str,
    body: AddVersionBody,
    service: PromptService = Depends(get_prompt_service),
) -> PromptVersionResponse:
    req = AddVersionRequest(prompt_id=prompt_id, content=body.content)
    return await service.add_version(req)


@router.put("/{prompt_id}/content", response_model=PromptVersionResponse)
async def update_content(
    prompt_id: str,
    body: UpdateContentBody,
    service: PromptService = Depends(get_prompt_service),
) -> PromptVersionResponse:
    req = UpdateContentRequest(prompt_id=prompt_id, content=body.content)
    return await service.update_content(req)


@router.post("/{prompt_id}/activate", response_model=PromptResponse)
async def activate_version(
    prompt_id: str,
    body: ActivateVersionBody,
    service: PromptService = Depends(get_prompt_service),
) -> PromptResponse:
    req = ActivateVersionRequest(prompt_id=prompt_id, version_id=body.version_id)
    return await service.activate_version(req)


@router.get("/active", response_model=list[PromptResponse])
async def list_active_prompts(
    service: PromptService = Depends(get_prompt_service),
) -> list[PromptResponse]:
    return await service.list_active_prompts(ListActivePromptsRequest())


@router.get("/deleted", response_model=list[PromptResponse])
async def list_deleted_prompts(
    service: PromptService = Depends(get_prompt_service),
) -> list[PromptResponse]:
    return await service.list_deleted_prompts(ListDeletedPromptsRequest())


@router.get("/{prompt_id}", response_model=PromptDetailResponse)
async def get_prompt_by_id(
    prompt_id: str,
    service: PromptService = Depends(get_prompt_service),
) -> PromptDetailResponse:
    req = GetPromptByIdRequest(prompt_id=prompt_id)
    return await service.get_prompt_by_id(req)


@router.get("/{prompt_id}/versions", response_model=list[PromptVersionResponse])
async def list_versions(
    prompt_id: str,
    service: PromptService = Depends(get_prompt_service),
) -> list[PromptVersionResponse]:
    req = ListVersionsRequest(prompt_id=prompt_id)
    return await service.list_versions(req)


@router.post("/{prompt_id}/compare", response_model=VersionDiffResponse)
async def compare_versions(
    prompt_id: str,
    body: CompareVersionsBody,
    service: PromptService = Depends(get_prompt_service),
) -> VersionDiffResponse:
    req = CompareVersionsRequest(
        prompt_id=prompt_id,
        version_id_before=body.version_id_before,
        version_id_after=body.version_id_after,
    )
    return await service.compare_versions(req)


@router.delete("/{prompt_id}", response_model=PromptResponse)
async def soft_delete_prompt(
    prompt_id: str,
    service: PromptService = Depends(get_prompt_service),
) -> PromptResponse:
    req = SoftDeletePromptRequest(prompt_id=prompt_id)
    return await service.soft_delete_prompt(req)


@router.post("/{prompt_id}/recover", response_model=PromptResponse)
async def recover_prompt(
    prompt_id: str,
    service: PromptService = Depends(get_prompt_service),
) -> PromptResponse:
    req = RecoverPromptRequest(prompt_id=prompt_id)
    return await service.recover_prompt(req)

