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

__all__ = ("config",)

from dataclasses import dataclass
import os

from dotenv import load_dotenv


@dataclass(frozen=True)
class ClientConfig(object):
    """Represents the configs for the bot

    .. versionadded:: 1.0.0

    Attributes
    ----------
    token : :class:`str`
        The token of the bot
    owner : :class:`int`
        The user ID of the owner
    color : :class:`int`
        The color value of embeds, etc.
    emoji_guild : :class:`int`
        An ID of a guild from which
        the bot retrieves its emojis.
        The bot has to be in this guild.


    .. note:: :class:`ClientConfig` is frozen
    """

    token: str
    owner: int
    color: int
    emoji_guild: int


load_dotenv()


config = ClientConfig(
    token=os.getenv("TOKEN"),  # type: ignore
    owner=int(os.getenv("OWNER")),  # type: ignore
    color=int(os.getenv("COLOR"), base=16),  # type: ignore
    emoji_guild=int(os.getenv("EMOJI_GUILD"))  # type: ignore
)
