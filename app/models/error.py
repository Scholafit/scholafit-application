
class ValidationError(Exception):
    
    def __init__(self, message:str, field=None) -> None:
        self.message = message
        self.field = field
        super().__init__(self.message)
    

    def __str__(self) -> str:
        if self.field:
            return f'ValidationError: {self.field} - {self.message}'
        return f'ValidationError: {self.message}'