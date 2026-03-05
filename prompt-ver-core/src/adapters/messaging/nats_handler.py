import dataclasses
import json
from collections.abc import Coroutine
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

import structlog
from nats.aio.client import Client as NatsClient
from nats.aio.msg import Msg

from src.adapters.persistence.unit_of_work import SqlAlchemyUnitOfWork
from src.app.activate_version import ActivateVersionUseCase
from src.app.add_version import AddVersionUseCase
from src.app.compare_versions import CompareVersionsUseCase
from src.app.create_prompt import CreatePromptUseCase
from src.app.dtos import (
    ActivateVersionCommand,
    AddVersionCommand,
    CompareVersionsQuery,
    CreatePromptCommand,
    GetPromptByIdQuery,
    ListVersionsQuery,
    RecoverPromptCommand,
    SoftDeletePromptCommand,
    UpdateContentCommand,
)
from src.app.exceptions import ApplicationException
from src.app.get_prompt_by_id import GetPromptByIdUseCase
from src.app.list_active_prompts import ListActivePromptsUseCase
from src.app.list_deleted_prompts import ListDeletedPromptsUseCase
from src.app.list_versions import ListVersionsUseCase
from src.app.recover_prompt import RecoverPromptUseCase
from src.app.soft_delete_prompt import SoftDeletePromptUseCase
from src.app.update_content import UpdateContentUseCase
from src.domain.exceptions import DomainException
from src.ports.event_publisher import EventPublisher

log = structlog.get_logger(__name__)

SUBJECTS = {
    "create_prompt": "prompts.v1.commands.create_prompt",
    "add_version": "prompts.v1.commands.add_version",
    "update_content": "prompts.v1.commands.update_content",
    "activate_version": "prompts.v1.commands.activate_version",
    "soft_delete_prompt": "prompts.v1.commands.soft_delete_prompt",
    "recover_prompt": "prompts.v1.commands.recover_prompt",
    "get_prompt_by_id": "prompts.v1.queries.get_prompt_by_id",
    "list_versions": "prompts.v1.queries.list_versions",
    "list_active_prompts": "prompts.v1.queries.list_active_prompts",
    "list_deleted_prompts": "prompts.v1.queries.list_deleted_prompts",
    "compare_versions": "prompts.v1.queries.compare_versions",
}


def _parse(data: bytes) -> dict:
    return json.loads(data.decode())


def _serialize(obj: Any) -> Any:
    if isinstance(obj, UUID):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return {f.name: _serialize(getattr(obj, f.name)) for f in dataclasses.fields(obj)}
    if isinstance(obj, (list, tuple)):
        return [_serialize(item) for item in obj]
    return obj


def _ok_response(result: Any) -> bytes:
    return json.dumps({"ok": True, "data": _serialize(result)}).encode()


def _error_response(code: str, message: str) -> bytes:
    return json.dumps({"ok": False, "error": {"code": code, "message": message}}).encode()


class NatsMessageHandler:
    def __init__(self, session_factory, publisher: EventPublisher) -> None:
        self._session_factory = session_factory
        self._publisher = publisher

    def _make_uow(self) -> SqlAlchemyUnitOfWork:
        return SqlAlchemyUnitOfWork(self._session_factory)

    async def _handle(self, msg: Msg, coro: Coroutine) -> None:
        correlation_id = (
            msg.headers.get("X-Correlation-Id") if msg.headers else None
        ) or str(uuid4())
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            correlation_id=correlation_id, subject=msg.subject
        )
        log.info("msg.received")
        try:
            result = await coro
            if msg.reply:
                await msg.respond(_ok_response(result))
        except (DomainException, ApplicationException) as exc:
            log.warning("msg.business_error", code=type(exc).__name__)
            if msg.reply:
                await msg.respond(_error_response(type(exc).__name__, str(exc)))
        except Exception:
            log.exception("msg.unexpected_error")
            if msg.reply:
                await msg.respond(_error_response("InternalError", "An unexpected error occurred"))

    async def on_create_prompt(self, msg: Msg) -> None:
        use_case = CreatePromptUseCase(self._make_uow(), self._publisher)
        body = _parse(msg.data)
        await self._handle(msg, use_case.execute(CreatePromptCommand(name=body["name"])))

    async def on_add_version(self, msg: Msg) -> None:
        use_case = AddVersionUseCase(self._make_uow(), self._publisher)
        body = _parse(msg.data)
        await self._handle(
            msg,
            use_case.execute(
                AddVersionCommand(
                    prompt_id=UUID(body["prompt_id"]),
                    content=body["content"],
                )
            ),
        )

    async def on_update_content(self, msg: Msg) -> None:
        use_case = UpdateContentUseCase(self._make_uow(), self._publisher)
        body = _parse(msg.data)
        await self._handle(
            msg,
            use_case.execute(
                UpdateContentCommand(
                    prompt_id=UUID(body["prompt_id"]),
                    content=body["content"],
                )
            ),
        )

    async def on_activate_version(self, msg: Msg) -> None:
        use_case = ActivateVersionUseCase(self._make_uow(), self._publisher)
        body = _parse(msg.data)
        await self._handle(
            msg,
            use_case.execute(
                ActivateVersionCommand(
                    prompt_id=UUID(body["prompt_id"]),
                    version_id=UUID(body["version_id"]),
                )
            ),
        )

    async def on_soft_delete_prompt(self, msg: Msg) -> None:
        use_case = SoftDeletePromptUseCase(self._make_uow(), self._publisher)
        body = _parse(msg.data)
        await self._handle(
            msg,
            use_case.execute(SoftDeletePromptCommand(prompt_id=UUID(body["prompt_id"]))),
        )

    async def on_recover_prompt(self, msg: Msg) -> None:
        use_case = RecoverPromptUseCase(self._make_uow(), self._publisher)
        body = _parse(msg.data)
        await self._handle(
            msg,
            use_case.execute(RecoverPromptCommand(prompt_id=UUID(body["prompt_id"]))),
        )

    async def on_get_prompt_by_id(self, msg: Msg) -> None:
        use_case = GetPromptByIdUseCase(self._make_uow())
        body = _parse(msg.data)
        await self._handle(
            msg,
            use_case.execute(GetPromptByIdQuery(prompt_id=UUID(body["prompt_id"]))),
        )

    async def on_list_versions(self, msg: Msg) -> None:
        use_case = ListVersionsUseCase(self._make_uow())
        body = _parse(msg.data)
        await self._handle(
            msg,
            use_case.execute(ListVersionsQuery(prompt_id=UUID(body["prompt_id"]))),
        )

    async def on_list_active_prompts(self, msg: Msg) -> None:
        use_case = ListActivePromptsUseCase(self._make_uow())
        await self._handle(msg, use_case.execute())

    async def on_list_deleted_prompts(self, msg: Msg) -> None:
        use_case = ListDeletedPromptsUseCase(self._make_uow())
        await self._handle(msg, use_case.execute())

    async def on_compare_versions(self, msg: Msg) -> None:
        use_case = CompareVersionsUseCase(self._make_uow())
        body = _parse(msg.data)
        await self._handle(
            msg,
            use_case.execute(
                CompareVersionsQuery(
                    prompt_id=UUID(body["prompt_id"]),
                    version_id_before=UUID(body["version_id_before"]),
                    version_id_after=UUID(body["version_id_after"]),
                )
            ),
        )

    async def subscribe_all(self, nc: NatsClient) -> list:
        return [
            await nc.subscribe(SUBJECTS["create_prompt"], cb=self.on_create_prompt),
            await nc.subscribe(SUBJECTS["add_version"], cb=self.on_add_version),
            await nc.subscribe(SUBJECTS["update_content"], cb=self.on_update_content),
            await nc.subscribe(SUBJECTS["activate_version"], cb=self.on_activate_version),
            await nc.subscribe(SUBJECTS["soft_delete_prompt"], cb=self.on_soft_delete_prompt),
            await nc.subscribe(SUBJECTS["recover_prompt"], cb=self.on_recover_prompt),
            await nc.subscribe(SUBJECTS["get_prompt_by_id"], cb=self.on_get_prompt_by_id),
            await nc.subscribe(SUBJECTS["list_versions"], cb=self.on_list_versions),
            await nc.subscribe(SUBJECTS["list_active_prompts"], cb=self.on_list_active_prompts),
            await nc.subscribe(SUBJECTS["list_deleted_prompts"], cb=self.on_list_deleted_prompts),
            await nc.subscribe(SUBJECTS["compare_versions"], cb=self.on_compare_versions),
        ]
