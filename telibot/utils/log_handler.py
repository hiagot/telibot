""" Logging handler for discord.py """
import logging
import logging.handlers
import os  # Add os module

# Create logs directory if it doesn't exist
LOGS_DIR = "telibot/logs"
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
logging.getLogger("discord.http").setLevel(logging.ERROR)

handler = logging.handlers.RotatingFileHandler(
    filename=os.path.join(LOGS_DIR, "discord.log"),
    encoding="utf-8",
    maxBytes=32 * 1024 * 1024,
    backupCount=5,
)
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter("[{asctime}] [{levelname:<8}] {name}: {message}", DATE_FORMAT, style="{")
handler.setFormatter(formatter)
