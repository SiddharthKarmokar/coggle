class CoggleError(Exception):
    """Base class for all custom exceptions."""
    pass

class KaggleAuthError(CoggleError):
    def __init__(self):
        super().__init__("[Error] Kaggle authentication failed. Make sure kaggle.json is in ~/.kaggle or credentials are in env vars.")
