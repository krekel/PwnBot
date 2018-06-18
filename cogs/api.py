import discord
import time
import datetime

from discord.ext import commands


class API:
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def ctf(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid ctf sub-command.')

    @ctf.command()
    async def upcoming(self, ctx, option: str):
        arguments = ('week', 'month', 'year')

        if option not in arguments:
            await ctx.send('Invalid argument for !ctf upcoming [argument]. Choose one of the following -> week, month or year')
            return

        embed = discord.Embed(colour=0x3DF270, title=f'Upcoming CTFs for this {option}')
        start, end = self._calculate_timestamp(option)

        # Get Request to ctf_time api to retrieve upcoming CTFs
        async with self.bot.session.get(f'https://ctftime.org/api/v1/events/?limit=100&start={start}&finish={end}') as response:
                upcoming = await response.json()
                for i, _ in enumerate(upcoming):
                    value = '\u2620' + upcoming[i]['title']
                    ctf_start = self.parse_date(upcoming[i]['start'])
                    ctf_end = self.parse_date(upcoming[i]['finish'])
                    ctf_date = f'Starts: {ctf_start}\nEnds: {ctf_end}'
                    embed.add_field(name=value, value=ctf_date, inline=False)
                    # embed.add_field(name=None, value='test')

        await ctx.send(content=None, embed=embed)

    @staticmethod
    def _calculate_timestamp(option):

        # TODO calculate seconds according to leap year, 30/31/28(9) day month
        # TODO fix hours so that upcoming will display correct events

        # 365 year and 30 days in a month
        temp = 86400
        seconds_in_a_week = 604800
        seconds_in_a_month = 2592000
        seconds_in_a_year = 31557600

        start = round(time.time())

        if option == 'month':
            return start, (start + seconds_in_a_month + temp)
        elif option == 'week':
            return start, (start + seconds_in_a_week + temp)
        elif option == 'year':
            return start, (start + seconds_in_a_year + temp)
        else:
            return

    @staticmethod
    def parse_date(date):
        """Parse dates provided by CTF TIME's API e.g 2018-05-05T00:00:00+00:00"""
        data = date.replace('T', ' ').replace('-', ' ').split(' ')
        year = int(data[0])
        month = int(data[1])
        day = int(data[2])

        time_ = data[3].split(':')
        hour = int(time_[0])
        minutes = int(time_[1])
        seconds = int(time_[2][0:2])

        p_date = datetime.datetime(year, month, day, hour, minutes, seconds)

        return p_date.strftime('%a,%d %b, %y %H:%M')


def setup(bot):
    bot.add_cog(API(bot))


