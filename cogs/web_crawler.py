import bs4
import discord
import json
import time


from discord.ext import commands


class WebCrawler:
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def ctf(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid ctf command.')

    @ctf.command()
    async def upcoming(self, ctx, option: str):
        arguments = ('week', 'month', 'year')

        if option not in arguments:
            await ctx.send('Invalid argument. Choose one of the following -> week, month or year')

        embed = discord.Embed(colour=0x3DF270, title=f'Upcoming CTFs for this {option}')
        start, end = self._calculate_timestamp(option)
        print(start, end)

        async with self.bot.session.get(f'https://ctftime.org/api/v1/events/?limit=100&start={start}&finish={end}') as response:
                upcoming = await response.json()
                for i, _ in enumerate(upcoming):
                    value = '\u2620' + upcoming[i]['title']
                    embed.add_field(name='', value=value, inline=True)

        await ctx.send(content=None, embed=embed)

    def _calculate_timestamp(self, option):

        # TODO calculate seconds according to leap year, 30/31/28(9) day month
        # TODO fix hours so that upcoming will display correct events

        # 365 year and 30 days in a month
        seconds_in_a_week = 604800
        seconds_in_a_month = 2592000
        seconds_in_a_year = 31557600

        start = round(time.time())

        if option == 'month':
            return start, (start + seconds_in_a_month)
        elif option == 'week':
            return start, (start + seconds_in_a_week)
        elif option == 'year':
            return start, (start + seconds_in_a_year)


def setup(bot):
    bot.add_cog(WebCrawler(bot))


