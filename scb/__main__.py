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

from pathlib import Path
import os
import sys

from dotenv import load_dotenv


PROJECT_DIR = str(Path(__file__).parents[1])

sys.path.insert(0, PROJECT_DIR)
os.chdir(PROJECT_DIR)


def main() -> None:
    load_dotenv()

    token = os.getenv("token")

    # The default color for embeds and such
    color = int(os.getenv("color", 0xf1f0ff), base=16)  # type: ignore

    # The ID of the guild from which the bot fetches its emojis
    emoji_guild = int(os.getenv("emoji_guild", 0))  # type: ignore

    from scb import SCBBot

    SCBBot(
        color=color,
        emoji_guild=emoji_guild
    ).run(token)


if __name__ == "__main__":
    major, minor = sys.version_info[:2]

    if major < 3 or minor < 8:
        raise Exception("^py39 required")

    main()
