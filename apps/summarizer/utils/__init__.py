from dataclasses import dataclass


@dataclass
class Result:
    """Contains information for the end user."""

    is_successful: bool = True
    message: str = ""

    def add_error(self, message: str) -> None:
        """Shortcut to add error message and mark it as unsuccessful."""
        self.is_successful = False
        self.message = message
