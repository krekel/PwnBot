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
        file = ctx.message.attachments[0]
        output = ''
        offset = 0

        async with self.bot.session.get(file.url) as resp:
            while True:
                chunk = await resp.read(16)
                if len(chunk) == 0:
                    break

                # offset
                output += f'{offset:#08x} '
                # hex content
                output += ' '.join(f'{ord(char):02x}' for char in chunk.decode('UTF-8')) + ' '
                # decoded text
                output += ''.join(f'{char}' if 32 < ord(char) < 128 else '.' for char in chunk.decode('UTF-8'))
                output += '\n'
                offset += 16

        # # Hex View
        # hexview = []
        # for x in range(2, len(data) + 2, 2):
        #     hexview.append(data[x - 2:x])
        #
        # if len(hexview) % 16 != 0:
        #     lines = (len(hexview) // 16) + 1
        # else:
        #     lines = len(hexview) // 16
        #
        # hexview.reverse()
        #
        # offset = 0x0
        # file_dump = ''
        # decoded_text = ''
        #
        # for _ in range(lines):
        #     # add the offset
        #     file_dump += str(hex(offset).replace('0x', '')).zfill(8) + ': '
        #     # add hex content with decoded text
        #     for _ in range(16):
        #         if len(hexview) != 0:
        #             byte = hexview.pop()
        #             decoded_text += byte
        #             file_dump += byte + ' '
        #             offset += 1
        #         else:
        #             break
        #     file_dump += bytearray.fromhex(decoded_text).decode() + '\n'
        #     decoded_text = ''
        # print(file_dump)

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

