import requests
import bs4
import discord

from discord.ext import commands


class WebCrawler:
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def ctf(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid ctf command.')

    @ctf.command()
    async def upcoming(self, ctx, filter_: str):
        await ctx.send('Upcoming ctfs...')

    async def _get_upcoming_ctfs(self, filter_):
        """
        Retrieve upcoming ctfs from CTF Time
        :return:
        """
        pass


def setup(bot):
    bot.add_cog(WebCrawler(bot))


