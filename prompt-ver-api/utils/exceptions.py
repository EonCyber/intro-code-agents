class BaseAppException(Exception):
    def __init__(
        self,
        message: str,
        error_code: str,
        http_status: int = 400,
        details: dict | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.http_status = http_status
        self.details = details or {}


class PromptNotFoundException(BaseAppException):
    def __init__(self, prompt_id: str) -> None:
        super().__init__(
            message=f"Prompt {prompt_id} não encontrado",
            error_code="PROMPT_NOT_FOUND",
            http_status=404,
        )


class VersionNotFoundException(BaseAppException):
    def __init__(self, version_id: str) -> None:
        super().__init__(
            message=f"Versão {version_id} não encontrada",
            error_code="VERSION_NOT_FOUND",
            http_status=404,
        )


class PromptAlreadyDeletedException(BaseAppException):
    def __init__(self, prompt_id: str) -> None:
        super().__init__(
            message=f"Prompt {prompt_id} já foi deletado",
            error_code="PROMPT_ALREADY_DELETED",
            http_status=409,
        )


class InvalidVersionComparisonException(BaseAppException):
    def __init__(self, detail: str = "") -> None:
        super().__init__(
            message="Comparação de versões inválida",
            error_code="INVALID_VERSION_COMPARISON",
            http_status=422,
            details={"detail": detail} if detail else {},
        )


class NATSPublishException(BaseAppException):
    def __init__(self, cause: str = "") -> None:
        super().__init__(
            message="Falha ao publicar evento",
            error_code="NATS_PUBLISH_ERROR",
            http_status=502,
            details={"cause": cause} if cause else {},
        )


class NATSRequestException(BaseAppException):
    def __init__(self, cause: str = "") -> None:
        super().__init__(
            message="Falha ao requisitar resposta via NATS",
            error_code="NATS_REQUEST_ERROR",
            http_status=502,
            details={"cause": cause} if cause else {},
        )
