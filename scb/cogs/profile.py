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

__all__ = ("Profile",)

from typing import TYPE_CHECKING
from datetime import datetime

from disnake.ext import commands
import disnake

if TYPE_CHECKING:
    from scb import SCBBot


class Profile(commands.Cog):
    __slots__ = ("bot",)

    def __init__(self, bot: "SCBBot") -> None:
        self.bot = bot

    @commands.slash_command(dm_permission=False)
    async def profile(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        member: disnake.Member
    ) -> None:
        """Show a members profile information

        Parameters
        ----------
        member: Show information about this member
        """

        avatar_url = member.display_avatar.url

        # Slice out "@everyone" and only list the 3 top roles
        roles = "\n".join(f"<@&{role.id}>" for role in member.roles[1:4])

        embed = disnake.Embed(
            title=member.display_name,
            description=f"Here's {member.mention}'s profile",
            color=self.bot.color,
            timestamp=datetime.now(),
        )
        embed.set_thumbnail(url=avatar_url)
        embed.add_field(
            name="Dates",
            value=f"Created: {member.created_at.date()}",
        )
        embed.add_field(
            name="Top 3 Roles",
            value=roles,
        )
        embed.add_field(
            name="ID",
            value=member.id,
            inline=False
        )
        embed.add_field(
            name="Rich-Kid",
            value=bool(member.premium_since)
        )
        embed.add_field(
            name="Is Bot",
            value=member.bot
        )
        embed.set_footer(
            text=f"{member!s}",
            icon_url=avatar_url
        )

        await interaction.send(embed=embed)


def setup(bot: "SCBBot") -> None:
    bot.add_cog(Profile(bot))
