import discord

from discord.ext import commands

POLL_PREFIX = '?'


class Poll:
    def __init__(self, bot):
        self.bot = bot
        # Active sessions
        self.sessions = []

    @commands.command()
    async def poll(self, ctx, topic: str, *, options: str):
        if self.get_session(ctx.channel) not in self.sessions:
            print(options)
            # TODO fix choices cleanup
            choices = [option for option in options.strip().split(' ')]
            poll_session = PollSession(self.bot, ctx.channel, topic, options)
            self.sessions.append(poll_session)

            await ctx.send(topic + " " + str(choices) + " " + str(ctx.channel))
        else:
            await ctx.send('There is an active poll in this channel.\n'
                           f'End it before creating another one. [!endpoll]')

    @commands.command(name='endpoll')
    async def end_poll(self, ctx):
        session = self.get_session(ctx.channel)
        await ctx.send(f'Poll session for channel {ctx.channel} has ended.\n'
                       f'Results {str(session.choices)}')

    async def on_message(self, message):
        if not message.author.bot:
            session = self.get_session(message.channel)
            if session and message.content.startswith(POLL_PREFIX):
                # count_votes
                session.check_vote(message.content)

    def get_session(self, channel):
        for session in self.sessions:
            if channel == session.channel:
                return session
        return None


class PollSession:
    def __init__(self, bot, channel, topic, choices):
        self.bot = bot
        self.channel = channel
        self.topic = topic
        self.choices = self._convert(choices)

    def check_vote(self, message: str):
        vote = message.replace('?', '').strip()

        if vote in self.choices.keys():
            self.choices[vote] += 1

    @staticmethod
    def _convert(lst) -> dict:
        choices = {}
        print(lst)
        for item in lst:
            print(item)
            choices[item] = 0

        print(choices)
        return choices

    def poll_results(self):
        pass


def setup(bot):
    bot.add_cog(Poll(bot))
