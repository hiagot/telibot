"""Helper function to play audio file and disconnect after playing"""

import asyncio

import discord


async def play_audio_file(member, file_path):
    """Helper function to play audio file and disconnect after playing"""
    if not member.voice or not member.voice.channel:
        print(f"Cannot connect: {member.name} is not in a voice channel")
        return

    try:
        vc = await member.voice.channel.connect()
        vc.play(discord.FFmpegPCMAudio(file_path))

        while vc.is_playing():
            await asyncio.sleep(0.1)
        await vc.disconnect()
    except Exception as err:
        print(f"Erro: {str(err)}")
        if "vc" in locals() and vc.is_connected():
            await vc.disconnect()
