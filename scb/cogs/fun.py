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

from typing import TYPE_CHECKING

from disnake.ext import commands
import disnake


if TYPE_CHECKING:
    from scb import SCBBot


class Fun(commands.Cog):
    __slots__ = ("bot",)

    def __init__(self, bot: "SCBBot"):
        self.bot = bot

    @commands.slash_command()
    async def exmatriculate(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ) -> None:
        """Wanna exmatriculate yourself? {{ EXMATRICULATE }}
        """

        view = disnake.ui.View()
        button = disnake.ui.Button(
            style=disnake.ButtonStyle.danger,
            label="Exmatriculate"
        )

        async def button_callback(button_interaction: disnake.MessageInteraction) -> None:
            button.disabled = True

            if button_interaction.author == interaction.author:
                await button_interaction.send("He seriously wants to leave :(")
            else:
                await button_interaction.send("EXMATRIKULIERT IHN / SIE!!")

            await interaction.edit_original_message(view=view)

        button.callback = button_callback
        view.add_item(button)

        await interaction.send(
            content=f"*{interaction.author.name}* wants to exmatriculate themselves",
            view=view
        )


def setup(bot: "SCBBot") -> None:
    bot.add_cog(Fun(bot))
