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

__all__ = ("Reaction",)

from typing import List, TYPE_CHECKING

from disnake.ext import commands
import disnake

if TYPE_CHECKING:
    from scb import SCBBot


class Reaction(commands.Cog):
    __slots__ = ("bot",)

    def __init__(self, bot: "SCBBot"):
        self.bot = bot

    @commands.slash_command(name="emoji", dm_permission=False)
    async def emoji_picker(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        emoji: str
    ) -> None:
        """Send the given emoji

        Parameters
        ----------
        emoji: The emoji you want to send
        """

        emojis = [emoji_ for emoji_ in interaction.guild.emojis if emoji_.name == emoji]

        if not emojis:
            return await interaction.send("Could not find the given emoji", ephemeral=True)

        await interaction.send(f"{emojis[0]!s}")

    @emoji_picker.autocomplete("emoji")
    async def autocomplete_emojis(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        user_input: str
    ) -> List[str]:
        emojis = [emoji.name for emoji in interaction.guild.emojis]

        return [emoji for emoji in emojis if user_input.lower() in emoji.lower()]


def setup(bot: "SCBBot") -> None:
    bot.add_cog(Reaction(bot))
