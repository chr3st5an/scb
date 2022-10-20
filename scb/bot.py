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

from typing import Any, Union, Optional
import os

from disnake.ext import commands
import disnake


HERE = os.path.dirname(__file__)


class SCBBot(commands.InteractionBot):
    def __init__(self, *, color: int, emoji_guild: int, **options: Any):
        """Create a SCBBot

        Parameters
        ----------
        color : :class:`int`
            The default (hex) color value for embeds, etc.
        emoji_guild : :class:`int`
            The ID of the guild from which the bot fetches
            its emojis
        **options : :class:`Any`
            Giveable options for :class:`disnake.InteractionBot`
        """

        super().__init__(
            max_messages=None,
            **options
        )
        self.__color = disnake.Colour(color)
        self.__emoji_guild = emoji_guild

        self.load_extensions(f"{HERE}/cogs")
        self.i18n.load("data/locale/")

    @property
    def color(self) -> disnake.Colour:
        """:class:`disnake.Colour` : The default color used for embeds, etc."""

        return self.__color

    @property
    def emoji_guild(self) -> int:
        """:class:`int` : The ID of the guild providing emojis for this bot"""

        return self.__emoji_guild

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
            guild = self.get_guild(self.emoji_guild)

            if guild is None:
                return None

            try:
                return [emoji for emoji in guild.emojis if emoji.name == emoji_id][0]
            except IndexError:
                return None

        return super().get_emoji(emoji_id)

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
