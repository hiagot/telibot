# Telibot, a discord bot! 🤖

## Purpose

* Make discord interactions more fun and provide some functionality.

## Features

* Play a sound whenever someone that is not connected to a voice channel joins any voice channel;
* Log in console when someone enter/leaves a voice chat;
* Slash command supported.

## Future Features

* Some moderation funcionality (like supect link removal) and SPAM detection;
* Support for sqlite or some external database like mariadb to record some events;
* Support to other languages. (It currently only supports brazilian portuguese);
* Documentation/tutorials.

## Contributions

The idea and execution of this bot came from TeliDev, feel free to contribute.

[![ImTeli](https://img.shields.io/badge/GitHub-ImTeli-blue)](https://github.com/ImTeli)

Special thanks to Rapptz the creator of discordpy (the API wrapper used to implement this bot.) and Its community.

[![discordpy](https://img.shields.io/badge/GitHub-Nextcord-blue)](https://github.com/Rapptz/discord.py)
## Requirements

In addition to the packages/modules present in the [pyproject.toml](https://github.com/ImTeli/telibot/blob/main/pyproject.toml) file, the "ffmpeg" program must be in the application's root folder.

The builds of this program can be found at: [ffmpeg](https://www.gyan.dev/ffmpeg/builds/)

Thank's to [Gyan.dev](https://github.com/GyanD) for the release builds.

You'll also need a Discord dev account, more details can be found at: https://docs.nextcord.dev/en/stable/discord.html

Python version: 

![Static Badge](https://img.shields.io/badge/Python-3.11%20%7C%203.12-blue)

## Console log example

```
#______________________________________________________________#
| Logged in as Telibot with id xxxxxxxxxxxxxxxxxxx
| Bot presente nos seguintes servidores:
| cantinho da interlocução id: xxxxxxxxxxxxxxxx
| Aldeia do Teli id: xxxxxxxxxxxxxxxxx
#______________________________________________________________#
Teli entrou no canal de voz Mesa 1 no servidor Aldeia do Teli em 2024-05-14 13:37:42.569062.
Teli saiu do canal de voz Mesa 1 no servidor Aldeia do Teli em 2024-05-14 13:37:51.555518.
```

## License

telibot_next uses the MIT license, click the badge for more details.

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/ImTeli/telibot_next/blob/main/LICENSE)
