import discord
from discord.ext import commands


class Info:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        await ctx.send('')


def setup(bot):
    bot.add_cog(Info(bot))
