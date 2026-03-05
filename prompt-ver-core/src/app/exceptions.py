from uuid import UUID


class ApplicationException(Exception):
    pass


class PromptNotFoundException(ApplicationException):
    def __init__(self, prompt_id: UUID):
        super().__init__(f"Prompt {prompt_id} not found")
        self.prompt_id = prompt_id
