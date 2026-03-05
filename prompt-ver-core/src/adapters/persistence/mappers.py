from src.adapters.persistence.orm_models import PromptORM, PromptVersionORM
from src.domain.enums import PromptStatus
from src.domain.prompt import Prompt
from src.domain.prompt_version import PromptVersion
from src.domain.value_objects import PromptContent, PromptName, VersionNumber


def orm_version_to_domain(row: PromptVersionORM) -> PromptVersion:
    return PromptVersion(
        id=row.id,
        prompt_id=row.prompt_id,
        version_number=VersionNumber(row.version_number),
        content=PromptContent(row.content),
        created_at=row.created_at,
        is_active=row.is_active,
    )


def orm_prompt_to_domain(row: PromptORM) -> Prompt:
    versions = [orm_version_to_domain(v) for v in row.versions]
    return Prompt(
        id=row.id,
        name=PromptName(row.name),
        status=PromptStatus(row.status),
        active_version_id=row.active_version_id,
        created_at=row.created_at,
        updated_at=row.updated_at,
        versions=versions,
    )


def domain_version_to_orm(version: PromptVersion) -> PromptVersionORM:
    return PromptVersionORM(
        id=version.id,
        prompt_id=version.prompt_id,
        version_number=version.version_number.value,
        content=version.content.value,
        created_at=version.created_at,
        is_active=version.is_active,
    )


def domain_prompt_to_orm(prompt: Prompt) -> PromptORM:
    orm_versions = [domain_version_to_orm(v) for v in prompt._versions]
    return PromptORM(
        id=prompt.id,
        name=prompt.name.value,
        status=prompt.status.value,
        active_version_id=prompt.active_version_id,
        created_at=prompt.created_at,
        updated_at=prompt.updated_at,
        versions=orm_versions,
    )
