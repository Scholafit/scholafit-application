
class ValidationError(Exception):
    
    def __init__(self, message:str, field=None) -> None:
        self.message = message
        self.field = field
        super().__init__(self.message)
    

    def __str__(self) -> str:
        if self.field:
            return f'ValidationError: {self.field} - {self.message}'
        return f'ValidationError: {self.message}'
    


class AiModelError(Exception):
    def __init__(self, message:str)-> None:
        self.message = message
        super().__init__(self.message)

    def __str__(self)-> str:
        return f'ai model api error: {self.message}' 