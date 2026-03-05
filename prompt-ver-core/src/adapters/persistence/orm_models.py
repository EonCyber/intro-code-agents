from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class PromptVersionORM(Base):
    __tablename__ = "prompt_versions"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    prompt_id: Mapped[UUID] = mapped_column(
        ForeignKey("prompts.id", ondelete="CASCADE"), nullable=False
    )
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class PromptORM(Base):
    __tablename__ = "prompts"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    status: Mapped[str] = mapped_column(
        Enum("ACTIVE", "INACTIVE", "DELETED", name="promptstatus"), nullable=False
    )
    active_version_id: Mapped[UUID | None] = mapped_column(
        ForeignKey(
            "prompt_versions.id",
            use_alter=True,
            name="fk_active_version",
        ),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    versions: Mapped[list[PromptVersionORM]] = relationship(
        PromptVersionORM,
        primaryjoin="PromptORM.id == PromptVersionORM.prompt_id",
        foreign_keys="PromptVersionORM.prompt_id",
        lazy="raise",
        cascade="all, delete-orphan",
    )
