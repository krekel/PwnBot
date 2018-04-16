import discord
from discord.ext import commands


class Info:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx):
        await ctx.send('Bot info')


def setup(bot):
    bot.add_cog(Info(bot))
