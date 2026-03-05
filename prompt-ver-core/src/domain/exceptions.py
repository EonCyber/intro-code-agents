from uuid import UUID


class DomainException(Exception):
    pass


class InvalidPromptContentException(DomainException):
    pass


class InvalidPromptNameException(DomainException):
    pass


class InvalidVersionNumberException(DomainException):
    pass


class VersionNotFoundException(DomainException):
    def __init__(self, version_id: UUID, prompt_id: UUID):
        super().__init__(f"Version {version_id} not found in prompt {prompt_id}")
        self.version_id = version_id
        self.prompt_id = prompt_id


class PromptDeletedException(DomainException):
    def __init__(self, prompt_id: UUID):
        super().__init__(f"Prompt {prompt_id} is deleted")
        self.prompt_id = prompt_id


class PromptAlreadyDeletedException(DomainException):
    def __init__(self, prompt_id: UUID):
        super().__init__(f"Prompt {prompt_id} is already deleted")
        self.prompt_id = prompt_id


class PromptNotDeletedException(DomainException):
    def __init__(self, prompt_id: UUID):
        super().__init__(f"Prompt {prompt_id} is not deleted")
        self.prompt_id = prompt_id
