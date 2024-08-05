from typing import List, Dict


class UnAuthorized(Exception):
    def __init__(self, message: str, details: List[Dict]) -> None:
        self.message = message
        self.details = details
        super().__init__()

    pass
