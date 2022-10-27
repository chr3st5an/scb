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

__all__ = ("Fun",)

from typing import TYPE_CHECKING, Dict, List, Optional
from datetime import datetime
import re
import asyncio
import secrets

from disnake.ext import tasks, commands
import aiohttp
import disnake


if TYPE_CHECKING:
    from scb import SCBBot


class Fun(commands.Cog):
    """Collection of commands that can be categorized as funny"""

    __slots__ = ("bot", "memes")

    def __init__(self, bot: "SCBBot"):
        self.bot = bot
        #             Category     URL
        #                 |         |
        self.memes: Dict[str, List[str]] = {
            "pigeon": []
        }

        self.fetch_memes.start()

    @tasks.loop(hours=6)
    async def fetch_memes(self) -> None:
        """Update the objects :attr:`memes` attribute every 6 hrs"""

        search_url = "https://tenor.com/search/{query}-gifs"

        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*[
                self.fetch_meme_category(
                    session,
                    search_url.format(query=category),
                    category
                ) for category in self.memes
            ])

    async def fetch_meme_category(
        self,
        session: aiohttp.ClientSession,
        search_url: str,
        store_as: str
    ) -> None:
        """Fetch meme URLs

        Make a request with the given session
        to the search url and evaluate the
        response. Afterwards, store all URLs
        in the objects :attr:`memes` attribute

        Parameters
        ----------
        session : :class:`aiohttp.ClientSession`
            The session used to make the request
        search_url : :class:`str`
            The URL to make a request to
        store_as : :class:`str`
            Store a list of URLs in the objects
            :attr:`memes` attribute under the given
            key name
        """

        url_regex = r'src="(https://media\..*?\.gif)"'

        async with session.get(search_url) as response:
            text = await response.text()

            try:
                # Clear previous cached memes
                self.memes[store_as].clear()
            except KeyError:
                self.memes[store_as] = []

            for url in re.findall(url_regex, text):
                self.memes[store_as].append(url)

            response.close()
            await response.wait_for_close()

    @commands.slash_command()
    async def exmatriculate(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ) -> None:
        """Wanna exmatriculate yourself? {{ EXMATRICULATE }}"""

        view = disnake.ui.View()
        button = disnake.ui.Button(
            style=disnake.ButtonStyle.danger,
            label="Exmatriculate"
        )

        async def button_callback(button_interaction: disnake.MessageInteraction) -> None:
            message = "EXMATRIKULIERT IHN / SIE!!"
            button.disabled = True

            if button_interaction.author == interaction.author:
                message = "He seriously wants to leave :("

            await button_interaction.send(message)
            await interaction.edit_original_message(view=view)

        button.callback = button_callback
        view.add_item(button)

        await interaction.send(
            content=f"*{interaction.author.name}* wants to exmatriculate themselves",
            view=view
        )

    @commands.slash_command()
    async def pigeon(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ) -> None:
        """Who doesn't like pigeons but Anna {{ PIGEON }}"""

        if not self.memes.get("pigeon"):
            return await interaction.send("No pigeons today :(", ephemeral=True)

        url = secrets.choice(self.memes["pigeon"])

        embed = disnake.Embed(
            title="PIGEOOONsss",
            type="gifv",
            color=self.bot.color,
            timestamp=datetime.now()
        )
        embed.set_image(url=url)
        embed.set_footer(text=str(interaction.author))

        button = disnake.ui.Button(
            label="Source",
            url=url
        )

        return await interaction.send(embed=embed, components=button)

    @commands.slash_command(name="hug")
    async def rick_roll(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        member: Optional[disnake.User] = commands.Param(None)
    ) -> None:
        """Send someone a hug <3 {{ HUG }}

        Parameters
        ----------
        member : :class:`member`
            The member you wanna hug {{ HUG_MEMBER }}
        """

        embed = disnake.Embed(
            type="gifv",
            color=self.bot.color,
            timestamp=datetime.now()
        )
        embed.set_image(
            url="https://media.tenor.com/pj2SpULBC7kAAAAd/loading-trolled.gif"
        )

        return await interaction.send(embed=embed, ephemeral=True)


def setup(bot: "SCBBot") -> None:
    bot.add_cog(Fun(bot))
