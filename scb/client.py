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

from typing import Dict, NoReturn, Union, Optional
import asyncio
import json
import os

from disnake.ext import commands
import disnake

from config import config


with open("data/emojis.json") as f:
    EMOJIS: Dict[str, str] = json.load(f)

HERE = os.path.dirname(__file__)


class SCBBot(commands.InteractionBot):
    def __init__(self, **kwargs):
        super().__init__(
            owner_id=config.owner,
            max_messages=None,
            **kwargs
        )
        self.color = disnake.Colour(config.color)

        self.load_extensions(f"{HERE}/cogs")

    def run(self) -> None:
        return super().run(config.token)

    def get_emoji(self, id_: Union[int, str], /) -> Optional[disnake.Emoji]:
        """Returns an emoji with the given ID.

        Parameters
        ----------
        id_ : :class:`Union[int, str]`
            The id to search for, or the name
            of an emoji found in `data/emojis.json`

        Returns
        -------
        :class:`Optional[Emoji]`
            The custom emoji or `None` if not found
        """

        if isinstance(id_, str):
            id_ = EMOJIS.get(id_)

        return super().get_emoji(id_)

    async def status_loop(self) -> NoReturn:
        """Constantly display two different statuses"""

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
                    name="with Christians mind",
                    type=disnake.ActivityType.playing
                )
            )
            await asyncio.sleep(60)

    async def on_ready(self) -> None:
        print(f"Logged in as {self.user}")

        asyncio.create_task(self.status_loop())
