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

__all__ = ("About",)

from typing import TYPE_CHECKING
from datetime import datetime

from disnake.ext import commands
import disnake


if TYPE_CHECKING:
    from scb import SCBBot


class About(commands.Cog):
    __slots__ = ("bot",)

    def __init__(self, bot: "SCBBot"):
        self.bot = bot

    @commands.slash_command()
    async def about(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ) -> None:
        """Generic information about the bot {{ ABOUT }}"""

        avatar = self.bot.user.avatar and self.bot.user.avatar.url
        app_info = await self.bot.application_info()

        embed = disnake.Embed(
            title="Generic Information",
            timestamp=datetime.now(),
            color=self.bot.color
        )
        embed.set_author(
            name=f"{self.bot.user}"
        )
        embed.set_thumbnail(
            url=avatar
        )
        embed.add_field(
            name="Maintainer",
            value=f"<@{self.bot.owner_id}>"
        )
        embed.add_field(
            name="Source Code",
            value="https://github.com/chr3st5an/scb"
        )
        embed.add_field(
            name="About",
            value=app_info.description or "-",
            inline=False
        )

        await interaction.send(embed=embed, ephemeral=True)


def setup(bot: "SCBBot") -> None:
    bot.add_cog(About(bot))
