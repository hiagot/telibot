import asyncio
import discord
import os
import discord.types

from datetime import datetime as dt
from dotenv import load_dotenv
from discord import (
    Activity,
    ActivityType,
    Interaction,
    Attachment,
    app_commands,
    Status,
)
from telibot.core.custom_exceptions import FileSizeException, NotAudioException
from telibot.utils.log_handler import handler
from telibot.core.teli_client import TeliClient


load_dotenv()

intents = discord.Intents.default()
teli_client = TeliClient(intents=intents)


@teli_client.event
async def on_ready():
    print("#" + "".center(70, "_") + "#")
    print(
        f"| \033[1;32mLogged in as {teli_client.user.name} with id {teli_client.user.id}\n\033[0m| \033[1;33mBot presente nos seguintes servidores:\033[0m"
    )
    for g in teli_client.guilds:
        print(f"| \033[0;33m{g} id: {g.id}\033[0m")
        if not os.path.exists(f"telibot/guilds/{g.id}"):
            os.makedirs(f"telibot/guilds/{g.id}")
            os.makedirs(f"telibot/guilds/{g.id}/sounds")
    print("#" + "".center(70, "_") + "#")
    await asyncio.sleep(10)
    await teli_client.change_presence(
        status=Status.online,
        activity=Activity(name="Teli programming me...", type=ActivityType(3)),
    )


@app_commands.describe(file="Arquivo de audio que irá tocar quando você entrar.")
@teli_client.tree.command(
    description="Insere um arquivo de áudio que toca toda vez que o usuário entra em alguma sala."
)
async def audio(interaction: Interaction, file: Attachment):
    await interaction.response.send_message(
        f"Processando arquivo: {file.filename}...", ephemeral=True
    )
    try:
        filepath = (
            f"telibot/guilds/{interaction.guild.id}/sounds/{interaction.user.id}.mp3"
        )
        if file is None:
            raise Exception(msg="Arquivo não recebido")
        elif not file.content_type.startswith("audio"):
            raise NotAudioException(file.content_type)
        elif file.size > 524288:
            raise FileSizeException(file.size, 524288)
        else:
            try:
                await file.save(filepath)
                await interaction.followup.send(
                    f"{interaction.user.mention} seu arquivo foi salvo com sucesso, entre e saia da sala"
                    f" para testar!",
                    ephemeral=True,
                )
            except Exception as n:
                await interaction.followup.send(
                    f"Erro durante a gravação do arquivo! Cód. Erro: {n}",
                    ephemeral=True,
                )
    except Exception as a:
        await interaction.followup.send(f"Error: {str(a)}", ephemeral=True)


@teli_client.event
async def on_voice_state_update(
    member: discord.Member, before: discord.VoiceState, after: discord.VoiceState
):
    if before.channel is None and member.global_name is not None:
        nome, canal, guilda = member.global_name, member.voice.channel, member.guild
        print(
            f"\033[0;32m{nome} entrou no canal de voz {canal} no servidor {guilda} em {dt.now()}.\033[0m"
        )

        if os.path.isfile(f"telibot/guilds/{member.guild.id}/sounds/{member.id}.mp3"):
            file_path = f"telibot/guilds/{member.guild.id}/sounds/{member.id}.mp3"
            try:
                vc = await member.voice.channel.connect()
                vc.play(discord.FFmpegPCMAudio(file_path))
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
        nome, canal, guilda = member.global_name, before.channel, member.guild
        print(
            f"\033[0;31m{nome} saiu do canal de voz {canal} no servidor {guilda} em {dt.now()}.\033[0m"
        )


if __name__ == "__main__":
    teli_client.run(os.getenv("TOKEN"), log_handler=handler)
