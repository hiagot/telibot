"""Client class for the bot."""
import discord
from discord import app_commands


class TeliClient(discord.Client):
    """Client class for the bot."""

    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
