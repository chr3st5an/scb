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

__all__ = ("Status",)

from typing import TYPE_CHECKING, NoReturn
import asyncio

from disnake.ext import commands
import disnake


if TYPE_CHECKING:
    from scb import SCBBot


class Status(commands.Cog):
    __slots__ = ("bot",)

    def __init__(self, bot: "SCBBot"):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        await asyncio.create_task(self.status_loop())

    async def status_loop(self) -> NoReturn:
        """Constantly display two different statuses sequentially"""

        while True:
            await self.bot.change_presence(
                activity=disnake.Activity(
                    name=f"{len(self.bot.guilds)} guilds",
                    type=disnake.ActivityType.watching
                )
            )
            await asyncio.sleep(60)

            await self.bot.change_presence(
                activity=disnake.Activity(
                    name=f"with {len(self.bot.slash_commands)} slash commands",
                    type=disnake.ActivityType.playing
                )
            )
            await asyncio.sleep(60)


def setup(bot: "SCBBot") -> None:
    bot.add_cog(Status(bot))
