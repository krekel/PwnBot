import discord
import binascii

from discord.ext import commands

HEX_PATH = '~/PycharmProjects/PwnBot/hexdumps'


class PwnTools:
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def tools(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid remind sub-command.')

    @tools.command()
    async def hexd(self, ctx):
        author = ctx.message.author
        file = ctx.message.attachments[0]
        output = ''
        offset = 0

        print(file.url)

        async with self.bot.session.get(file.url) as resp:
            while True:
                chunk = await resp.content.read(16)
                print(chunk)
                if len(chunk) == 0:
                    break

                # offset
                output += f'{offset:#08x} '
                # hex content
                output += ' '.join(f'{ord(char):02x}' for char in chunk.decode('ISO-8859-1')) + ' '
                # decoded text
                output += ''.join(f'{char}' if 32 < ord(char) < 128 else '.' for char in chunk.decode('ISO-8859-1'))
                output += '\n'
                offset += 16
        print(output)

        await ctx.send(output)

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

