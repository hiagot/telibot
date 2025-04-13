""" Main file of the bot. """
import asyncio
import os
import pathlib
from datetime import datetime as dt

import discord
from discord import (
    Activity,
    ActivityType,
    Attachment,
    Interaction,
    Status,
    app_commands,
)
from discord.errors import Forbidden, InvalidData

from telibot.core.client import TeliClient
from telibot.core.requests import post_guild, post_message, post_user
from telibot.exceptions import FileSizeException, NotAudioException
from telibot.settings import get_settings
from telibot.utils import play_audio_file


intents = discord.Intents.all()
teli_client = TeliClient(intents=intents)


@teli_client.event
async def on_ready():
    """ Starting routine when the bot is ready. """
    print("#" + "".center(70, "_") + "#")
    print(f"| \033[1;32mLogged in as {teli_client.user.name} with id {teli_client.user.id}\n\033[0m| \033[1;33mBot present in the following servers:\033[0m")
    for g in teli_client.guilds:
        print(f"| \033[0;33m{g} id: {g.id}\033[0m")
        if not os.path.exists(f"telibot/guilds/{g.id}"):
            os.makedirs(f"telibot/guilds/{g.id}")
            os.makedirs(f"telibot/guilds/{g.id}/sounds")
        post_user(user=g.owner)
        post_guild(guild=g)
        for user in g.members:
            post_user(user=user)
    print("#" + "".center(70, "_") + "#")

    await asyncio.sleep(10)
    await teli_client.change_presence(status=Status.online, activity=Activity(name="Teli programming me...", type=ActivityType(3)))


@app_commands.describe(file="Arquivo de audio que irá tocar quando você entrar.")
@teli_client.tree.command(description="Insere um arquivo de áudio que toca toda vez que o usuário entra em alguma sala.")
async def audio(interaction: Interaction, file: Attachment):
    """ Command to insert an audio file that plays every time the user enters a voice channel. """
    await interaction.response.send_message(f"Processando arquivo: {file.filename}...", ephemeral=True)
    try:
        filepath = pathlib.Path(os.path.join("telibot", "guilds", str(interaction.guild_id), "sounds", f"{interaction.user.id}.mp3"))
        if file is None:
            raise ValueError("Arquivo não recebido")

        if file.content_type is None or not file.content_type.startswith("audio"):
            raise NotAudioException(file.content_type or "None")

        if file.size > 524288:
            raise FileSizeException(file.size, 524288)

        try:
            await file.save(filepath)
            await interaction.followup.send(f"{interaction.user.mention} seu arquivo foi salvo com sucesso, entre e saia da sala para testar!", ephemeral=True)

        except Forbidden as n:
            await interaction.followup.send(f"Permissão negada! Cód. Erro: {n}",ephemeral=True)

        except discord.HTTPException as n:
            await interaction.followup.send(f"Erro durante a gravação do arquivo! Cód. Erro: {n}",ephemeral=True)

        except InvalidData as n:
            await interaction.followup.send(f"Arquivo inválido! Cód. Erro: {n}",ephemeral=True)

    except ValueError as a:
        await interaction.followup.send(f"Error: {str(a)}", ephemeral=True)

    except Exception as a:
        await interaction.followup.send(f"Erro inesperado: {str(a)}", ephemeral=True)

@teli_client.event
async def on_message(message: discord.Message):
    """ Event that triggers when a message is sent. """
    if message.author == teli_client.user:
        return

    post_message(message=message)


@teli_client.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    """Event that triggers when a user enters or leaves a voice channel."""

    if before.channel is None and after.channel is not None and member.global_name:
        name = member.global_name
        guild = member.guild
        channel = member.voice.channel if member.voice else None

        print(f"\033[0;32m{name} entrou no canal de voz {channel} no servidor {guild} em {dt.now().strftime('%d/%m/%Y às %H:%M:%S')}.\033[0m")

        file_path = f"telibot/guilds/{member.guild.id}/sounds/{member.id}.mp3"
        if os.path.isfile(file_path):
            await play_audio_file(member, file_path)

    elif before.channel is not None and after.channel is None and member.global_name:
        name = member.global_name
        guild = member.guild
        channel = before.channel

        print(f"{name} saiu do canal de voz {channel} no servidor {guild} em {dt.now().strftime('%d/%m/%Y às %H:%M:%S')}.")

if __name__ == "__main__":
    teli_client.run(get_settings().DISCORD_BOT_TOKEN)
