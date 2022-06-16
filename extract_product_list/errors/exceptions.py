class ExcelFileNoFound(Exception):
    
    def __init__(self, message: str):
        super().__init__()
        self.message = message
    
    def __str__(self) -> str:
        return '%s' % self.message

class ExcelContentNoSupported(Exception):
    def __init__(self, message: str):
        super().__init__()
        self.message = message
    
    def __str__(self) -> str:
        return '%s' % self.message