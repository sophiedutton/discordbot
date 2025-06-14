# Simple Discord bot for collecting bunnies
# Requires discord.py

import os
import json
import asyncio

import discord
from discord.ext import commands

DATA_FILE = "bunnies.json"


class BunnyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)
        self.bunnies = {}

    async def setup_hook(self):
        await self.load_data()
        self.add_command(self.collect)
        self.add_command(self.bunnies_cmd)
        self.add_command(self.leaderboard)

    async def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                self.bunnies = json.load(f)
        else:
            self.bunnies = {}

    async def save_data(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.bunnies, f)

    async def close(self):
        await self.save_data()
        await super().close()

    @commands.command(name="collect")
    async def collect(self, ctx: commands.Context):
        user_id = str(ctx.author.id)
        self.bunnies[user_id] = self.bunnies.get(user_id, 0) + 1
        await ctx.send(f"{ctx.author.mention} collected a bunny! Total: {self.bunnies[user_id]}")

    @commands.command(name="bunnies")
    async def bunnies_cmd(self, ctx: commands.Context):
        user_id = str(ctx.author.id)
        count = self.bunnies.get(user_id, 0)
        await ctx.send(f"{ctx.author.mention} has {count} bunnies.")

    @commands.command(name="leaderboard")
    async def leaderboard(self, ctx: commands.Context):
        if not self.bunnies:
            await ctx.send("No bunnies collected yet!")
            return
        top = sorted(self.bunnies.items(), key=lambda item: item[1], reverse=True)[:5]
        lines = []
        for i, (user_id, count) in enumerate(top, 1):
            user = await self.fetch_user(int(user_id))
            lines.append(f"{i}. {user.name}: {count}")
        await ctx.send("\n".join(lines))


async def main():
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("DISCORD_TOKEN environment variable is not set")
    bot = BunnyBot()
    async with bot:
        await bot.start(token)


if __name__ == "__main__":
    asyncio.run(main())
