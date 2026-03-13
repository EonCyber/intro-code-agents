from messaging.nats_publisher import NATSPublisher
from models.prompt_models import (
    ActivateVersionRequest,
    AddVersionRequest,
    CompareVersionsRequest,
    CreatePromptRequest,
    DiffLineResponse,
    EventWrapper,
    GetPromptByIdRequest,
    ListActivePromptsRequest,
    ListDeletedPromptsRequest,
    ListVersionsRequest,
    PromptDetailResponse,
    PromptResponse,
    PromptVersionResponse,
    RecoverPromptRequest,
    SoftDeletePromptRequest,
    UpdateContentRequest,
    VersionDiffResponse,
)


class PromptService:
    def __init__(self, publisher: NATSPublisher) -> None:
        self.publisher = publisher

    async def create_prompt(self, req: CreatePromptRequest) -> PromptResponse:
        payload = {
            "name": req.name,
            "content": req.content,
        }
        raw = await self.publisher.request("prompts.v1.commands.create_prompt", payload)
        return EventWrapper[PromptResponse](**raw).data

    async def add_version(self, req: AddVersionRequest) -> PromptVersionResponse:
        payload = {
            "prompt_id": req.prompt_id,
            "content": req.content,
        }
        raw = await self.publisher.request("prompts.v1.commands.add_version", payload)
        return EventWrapper[PromptVersionResponse](**raw).data

    async def update_content(self, req: UpdateContentRequest) -> PromptVersionResponse:
        payload = {
            "prompt_id": req.prompt_id,
            "content": req.content,
        }
        raw = await self.publisher.request("prompts.v1.commands.update_content", payload)
        return EventWrapper[PromptVersionResponse](**raw).data

    async def activate_version(self, req: ActivateVersionRequest) -> PromptResponse:
        payload = {
            "prompt_id": req.prompt_id,
            "version_id": req.version_id,
        }
        raw = await self.publisher.request("prompts.v1.commands.activate_version", payload)
        return EventWrapper[PromptResponse](**raw).data

    async def get_prompt_by_id(self, req: GetPromptByIdRequest) -> PromptDetailResponse:
        payload = {
            "prompt_id": req.prompt_id,
        }
        raw = await self.publisher.request("prompts.v1.queries.get_prompt_by_id", payload)
        return EventWrapper[PromptDetailResponse](**raw).data

    async def list_versions(self, req: ListVersionsRequest) -> list[PromptVersionResponse]:
        payload = {
            "prompt_id": req.prompt_id,
        }
        raw = await self.publisher.request("prompts.v1.queries.list_versions", payload)
        return EventWrapper[list[PromptVersionResponse]](**raw).data

    async def list_active_prompts(self, req: ListActivePromptsRequest) -> list[PromptResponse]:
        payload: dict = {}
        raw = await self.publisher.request("prompts.v1.queries.list_active_prompts", payload)
        return EventWrapper[list[PromptResponse]](**raw).data

    async def compare_versions(self, req: CompareVersionsRequest) -> VersionDiffResponse:
        payload = {
            "prompt_id": req.prompt_id,
            "version_id_before": req.version_id_before,
            "version_id_after": req.version_id_after,
        }
        raw = await self.publisher.request("prompts.v1.queries.compare_versions", payload)
        return EventWrapper[VersionDiffResponse](**raw).data

    async def soft_delete_prompt(self, req: SoftDeletePromptRequest) -> PromptResponse:
        payload = {
            "prompt_id": req.prompt_id,
        }
        raw = await self.publisher.request("prompts.v1.commands.soft_delete_prompt", payload)
        return EventWrapper[PromptResponse](**raw).data

    async def list_deleted_prompts(self, req: ListDeletedPromptsRequest) -> list[PromptResponse]:
        payload: dict = {}
        raw = await self.publisher.request("prompts.v1.queries.list_deleted_prompts", payload)
        return EventWrapper[list[PromptResponse]](**raw).data

    async def recover_prompt(self, req: RecoverPromptRequest) -> PromptResponse:
        payload = {
            "prompt_id": req.prompt_id,
        }
        raw = await self.publisher.request("prompts.v1.commands.recover_prompt", payload)
        return EventWrapper[PromptResponse](**raw).data

