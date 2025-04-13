"""This module contains utility functions for the bot."""
import logging
import os
from datetime import datetime

import discord
import requests

from telibot.settings import get_settings

USER_BEHAVIOR = 25
logging.addLevelName(USER_BEHAVIOR, "USER_BEHAVIOR")

class BotLogHandler(logging.Handler):
    """Handler for the bot logs."""
    def __init__(self, level: int = logging.NOTSET) -> None:
        super().__init__(level)
        log_dir: str = "logs"
        os.makedirs(log_dir, exist_ok=True)
        log_filename: str = datetime.now().strftime("%d-%m-%Y-%H-%M-%S-%f") + ".log"
        self.log_filepath: str = os.path.join(log_dir, log_filename)

    def emit(self, record: logging.LogRecord) -> None:
        log_entry: str = self.format(record)
        with open(self.log_filepath, "a", encoding="utf-8") as log_file:
            log_file.write(log_entry + "\n")

    def log_message(self, message: str | dict, level: int = logging.NOTSET) -> None:
        """Log a message."""
        logger = logging.getLogger()
        log_record = logger.makeRecord(
            name=logger.name,
            fn="",
            lno=0,
            level=level,
            msg=message,
            args=(),
            exc_info=None,
            func=None,
            sinfo=None,
        )
        self.emit(log_record)

def post_guild(guild: discord.Guild) -> dict:
    """Post a guild to the API."""
    payload = {
            "guild_id": str(guild.id),
            "guild_name": guild.name,
            "guild_owner": str(guild.owner_id),
            "guild_icon": str(""),
            "guild_member_count": guild.member_count,
            "guild_created_at": guild.created_at.isoformat()
        }
    resp = requests.post(f"http://{get_settings().API_URL}/guilds/", json=payload, timeout=2)
    try:
        response_data = resp.json() if resp.content else {}
    except requests.exceptions.JSONDecodeError:
        response_data = {}
    return {"status_code": resp.status_code, "response": response_data}

def post_user(user: discord.Member) -> dict:
    """Post a user to the API."""
    payload = {
                "discord_id": str(user.id),
                "global_name": str(user.global_name),
                "avatar": "",
                "is_bot" : user.bot
            }
    resp = requests.post(f"http://{get_settings().API_URL}/users/create_user", json=payload, timeout=2)
    try:
        response_data = resp.json() if resp.content else {}
    except requests.exceptions.JSONDecodeError:
        response_data = {}
    return {"status_code": resp.status_code, "response": response_data}

def post_message(message: discord.Message) -> dict:
    """Post a message to the API."""
    payload = {
        "member_id": str(message.author.id) if message.author else None,
        "guild_id": str(message.guild.id) if message.guild else None,
        "channel_id": str(message.channel.id) if message.channel else None,
        "channel_name": str(message.channel.name) if message.channel else None, # type: ignore[union-attr]
        "message_content": str(message.content) if message.content else None
    }

    resp = requests.post(f"http://{get_settings().API_URL}/messages/add_message", json=payload, timeout=2)
    return {"status_code": resp.status_code, "response": resp.json()}
