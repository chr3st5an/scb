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

__all__ = ("Websites",)

from typing import Dict, TYPE_CHECKING
import json
import secrets

from disnake.ext import commands
import disnake


if TYPE_CHECKING:
    from scb import SCBBot


MOODLE_COURSE_BASE_URL = "https://moodle.uni-due.de/course/view.php?id="

with open("data/uni-links.json") as f:
    data: Dict[str, str] = json.load(f)

    websites = commands.option_enum(
       dict(sorted(data.items()))
    )

with open("data/moodle-courses.json") as f:
    data: Dict[str, str] = json.load(f)

    courses = commands.option_enum(
        {k: MOODLE_COURSE_BASE_URL + v for k, v in data.items()}
    )


class Websites(commands.Cog):
    __slots__ = ("bot",)

    def __init__(self, bot: "SCBBot"):
        self.bot = bot

    async def send_link(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        link: str
    ) -> None:
        """Sends a message with a button to the given interaction"""

        action_row = disnake.ui.ActionRow()
        action_row.add_button(
            label="Open",
            url=link
        )
        emoji = self.bot.get_emoji(
            secrets.choice(
                [
                    "internetexplorer",
                    "wumpus_gift",
                    "www",
                ]
            )
        )

        await interaction.send(
            content=f"Here you go! {emoji}",
            components=action_row,  # type: ignore
            ephemeral=True,
        )

    @commands.slash_command()
    async def websites(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        website: "websites"
    ) -> None:
        """Search for a uni related webpage {{ WEBSITES }}

        Parameters
        ----------
        website: The website you are looking for {{ WEBSITES_WEBSITE }}
        """

        await self.send_link(interaction, website)

    @commands.slash_command()
    async def moodle(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        course: "courses"
    ) -> None:
        """Search a Moodle course {{ MOODLE }}

        Parameters
        ----------
        course: The Moodle course you are looking for {{ MOODLE_COURSE }}
        """

        await self.send_link(interaction, course)


def setup(bot: "SCBBot") -> None:
    bot.add_cog(Websites(bot))
