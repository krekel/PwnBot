import discord
import binascii

from discord.ext import commands

HEX_PATH = '~/PycharmProjects/PwnBot/hexdumps'
RECV_PATH = '~/PycharmProjects/PwnBot/recv_files'


class PwnTools:
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def tools(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid remind sub-command.')

    @tools.command()
    async def hexd(self, ctx):
        file = ctx.message.attachments[0]

        async with self.bot.session.get(file.url) as resp:
            data = await resp.read()
            data = binascii.hexlify(data).decode('UTF-8')

        # Hex View
        hexview = []
        for x in range(2, len(data) + 2, 2):
            hexview.append(data[x - 2:x])

        if len(hexview) % 16 != 0:
            lines = (len(hexview) // 16) + 1
        else:
            lines = len(hexview) // 16

        hexview.reverse()

        offset = 0x0
        file_dump = ''

        for _ in range(lines):
            # add the offset
            file_dump += str(hex(offset).replace('0x', '')).zfill(8) + ': '
            # add hex content
            for _ in range(16):
                if len(hexview) != 0:
                    file_dump += hexview.pop() + ' '
                    offset += 1
                else:
                    break
            file_dump += '\n'
        print(file_dump)

        await ctx.send(file_dump)

    @tools.command()
    async def b64e(self, ctx, plaintext):
        pass

    @tools.command()
    async def b64d(self, ctx, encoded_string):
        pass

    @tools.command()
    async def delete(self, ctx, reminder_id):
        pass


def setup(bot):
    bot.add_cog(PwnTools(bot))

