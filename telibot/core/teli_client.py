import discord
from discord import app_commands


class TeliClient(discord.Client):
    def __init__(self, *, intents: discord.Intents, test: discord.Object = None):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.test = test

    async def setup_hook(self):
        if self.test is not None:
            await self.tree.sync(guild=self.test)
            self.tree.copy_global_to(guild=self.test)
        else:
            await self.tree.sync()
