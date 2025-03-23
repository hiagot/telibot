"""Main file of the project."""

import asyncio
import os
import pathlib
from datetime import datetime as dt

import discord
import discord.types
from discord import (
    Activity,
    ActivityType,
    Attachment,
    Interaction,
    Status,
    VoiceClient,
    app_commands,
)

from telibot.core.custom_exceptions import FileSizeException, NotAudioException
from telibot.core.teli_client import TeliClient
from telibot.settings import get_settings

SETTINGS = get_settings()

intents = discord.Intents.default()
teli_client = TeliClient(intents=intents)


@teli_client.event
async def on_ready():
    """Event that runs when the bot is ready."""
    print("#" + "".center(70, "_") + "#")
    print(f"| \033[1;32mLogged in as {teli_client.user.name} with id {teli_client.user.id}\n\033[0m| \033[1;33mBot presente nos seguintes servidores:\033[0m")
    for g in teli_client.guilds:
        print(f"| \033[0;33m{g} id: {g.id}\033[0m")
        if not os.path.exists(f"telibot/guilds/{g.id}"):
            os.makedirs(f"telibot/guilds/{g.id}")
            os.makedirs(f"telibot/guilds/{g.id}/sounds")
    print("#" + "".center(70, "_") + "#")
    await asyncio.sleep(10)
    await teli_client.change_presence(status=Status.online, activity=Activity(name="Teli programming me...", type=ActivityType(3)))


@app_commands.describe(file="Arquivo de audio que irá tocar quando você entrar.")
@teli_client.tree.command(description="Insere um arquivo de áudio que toca toda vez que o usuário entra em alguma sala.")
async def audio(interaction: Interaction, file: Attachment):
    """Command that receives an audio file and saves it to play when the user enters a voice channel."""
    await interaction.response.send_message(f"Processando arquivo: {file.filename}...", ephemeral=True)
    try:
        filepath = pathlib.Path(os.path.join("telibot", "guilds", str(interaction.guild_id), "sounds", f"{interaction.user.id}.mp3"))
        if file is None:
            raise FileNotFoundError(msg="Arquivo não recebido")
        if file.content_type is None or not file.content_type.startswith("audio"):
            raise NotAudioException(file.content_type or "None")
        if file.size > 524288:
            raise FileSizeException(file.size, 524288)
        try:
            await file.save(filepath)
            await interaction.followup.send(f"{interaction.user.mention} seu arquivo foi salvo com sucesso, entre e saia da sala para testar!", ephemeral=True)
        except Exception as n:
            await interaction.followup.send(
                f"Erro durante a gravação do arquivo! Cód. Erro: {n}",
                ephemeral=True,
            )
    except Exception as a:
        await interaction.followup.send(f"Error: {str(a)}", ephemeral=True)


@teli_client.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    """Event that runs when a member enters or leaves a voice channel."""
    if before.channel is None and member.global_name is not None:
        name = member.global_name
        guilda = member.guild
        canal = member.voice.channel if member.voice else None
        print(f"\033[0;32m{name} entrou no canal de voz {canal} no servidor {guilda} em {dt.now()}.\033[0m")

        if os.path.isfile(f"telibot/guilds/{member.guild.id}/sounds/{member.id}.mp3"):
            file_path = f"telibot/guilds/{member.guild.id}/sounds/{member.id}.mp3"
            try:
                if member.voice and member.voice.channel:
                    vc: VoiceClient = await member.voice.channel.connect()
                else:
                    print(f"Cannot connect: {member.name} is not in a voice channel")
                    return
                vc.play(discord.FFmpegPCMAudio(file_path)) #type: ignore
                while True:
                    await asyncio.sleep(0.01)
                    try:
                        if not vc.is_playing():
                            await vc.disconnect()
                            break
                    except UnboundLocalError:
                        pass
            except Exception as err:
                print(f"Erro: {str(err)}")

    elif (
        before.channel is not None and after.channel is None
    ) and member.global_name is not None:
        name, canal, guilda = member.global_name, before.channel, member.guild
        print(
            f"\033[0;31m{name} saiu do canal de voz {canal} no servidor {guilda} em {dt.now()}.\033[0m"
        )


if __name__ == "__main__":
    teli_client.run(SETTINGS.TOKEN)
