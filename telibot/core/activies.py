""" List of bot activities. """
from typing import Any
from discord import BaseActivity, ActivityType


class DefaultActivity(BaseActivity):
    """Default activity for the bot."""
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.type = ActivityType(3)
        self.name = "Teli programming me..."
        self.url = "https://github.com/ImTeli/telibot"
