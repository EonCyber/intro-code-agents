from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.adapters.persistence.mappers import domain_prompt_to_orm, orm_prompt_to_domain
from src.adapters.persistence.orm_models import PromptORM
from src.domain.enums import PromptStatus
from src.domain.prompt import Prompt
from src.ports.prompt_repository import PromptRepository


class SqlAlchemyPromptRepository(PromptRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, prompt_id: UUID) -> Prompt | None:
        stmt = (
            select(PromptORM)
            .where(PromptORM.id == prompt_id)
            .options(selectinload(PromptORM.versions))
        )
        result = await self._session.execute(stmt)
        row = result.scalar_one_or_none()
        if row is None:
            return None
        return orm_prompt_to_domain(row)

    async def save(self, prompt: Prompt) -> None:
        orm_obj = domain_prompt_to_orm(prompt)
        await self._session.merge(orm_obj)

    async def list_by_status(self, status: PromptStatus) -> list[Prompt]:
        stmt = (
            select(PromptORM)
            .where(PromptORM.status == status.value)
            .options(selectinload(PromptORM.versions))
            .order_by(PromptORM.created_at.desc())
        )
        result = await self._session.execute(stmt)
        rows = result.scalars().all()
        return [orm_prompt_to_domain(row) for row in rows]
