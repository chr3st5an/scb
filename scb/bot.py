"""
MIT License

Copyright (c) 2022 chr3st5an

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

__all__ = ("SCBBot",)

from typing import Union, NoReturn, Optional
import os
import asyncio

from disnake.ext import commands
import disnake

from scb.config import config


HERE = os.path.dirname(__file__)


class SCBBot(commands.InteractionBot):
    def __init__(self, **options):
        super().__init__(
            owner_id=config.owner,
            max_messages=None,
            **options
        )
        self.color = disnake.Colour(config.color)

        self.load_extensions(f"{HERE}/cogs")
        self.i18n.load("data/locale/")

    def run(self) -> None:
        return super().run(config.token)

    def get_emoji(self, emoji_id: Union[int, str], /) -> Optional[disnake.Emoji]:
        """Returns an emoji with the given ID.

        Parameters
        ----------
        id_ : :class:`Union[int, str]`
            The id to search for, or the name
            of an emoji found in the provided
            emoji guild

        Returns
        -------
        :class:`Optional[Emoji]`
            The custom emoji or `None` if not found
        """

        if isinstance(emoji_id, str):
            guild = self.get_guild(config.emoji_guild)

            if guild is None:
                return None

            try:
                return [emoji for emoji in guild.emojis if emoji.name == emoji_id][0]
            except IndexError:
                return None

        return super().get_emoji(emoji_id)

    async def status_loop(self) -> NoReturn:
        """Constantly display two different statuses sequentially"""

        while True:
            await self.change_presence(
                activity=disnake.Activity(
                    name=f"{len(self.guilds)} guilds",
                    type=disnake.ActivityType.watching
                )
            )
            await asyncio.sleep(60)

            await self.change_presence(
                activity=disnake.Activity(
                    name=f"with {len(self.slash_commands)} slash commands",
                    type=disnake.ActivityType.playing
                )
            )
            await asyncio.sleep(60)

    async def on_ready(self) -> None:
        print(f"Logged in as {self.user}")

        asyncio.create_task(self.status_loop())

    async def on_slash_command_error(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        exception: commands.CommandError
    ) -> None:
        if isinstance(exception, commands.NoPrivateMessage):
            return await interaction.send(
                "For this command to work, the bot needs to be on this server",
                ephemeral=True
            )

        await interaction.send("An error occurred", ephemeral=True)
