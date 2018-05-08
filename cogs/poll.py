import discord

from discord.ext import commands

POLL_PREFIX = '?'


class Poll:
    def __init__(self, bot):
        self.bot = bot
        # Active sessions
        self.sessions = []

    @commands.has_any_role('Mod', 'Admin')
    @commands.command()
    async def poll(self, ctx, topic: str, *, options: str):
        if self.get_session(ctx.channel) not in self.sessions:

            choices = [option.upper() for option in options.strip().split(' ')]
            poll_session = PollSession(self.bot, ctx.channel, topic, choices)
            self.sessions.append(poll_session)

            await ctx.send(f'Poll session started!\n'
                           f'Topic: {topic}\n'
                           f'Voting Options: {str(choices)}\n'
                           f'To vote type ?[choice]')
        else:
            await ctx.send('There is an active poll in this channel.\n'
                           f'End it before creating another one. [!endpoll]')

    @commands.has_any_role('Mod', 'Admin')
    @commands.command(name='endpoll')
    async def end_poll(self, ctx):
        session = self.get_session(ctx.channel)
        self.sessions.remove(session)
        await ctx.send(f'Poll session for channel {ctx.channel} has ended.\n'
                       f'{session.poll_results()}')

    async def on_message(self, message):
        if not message.author.bot:
            session = self.get_session(message.channel)
            if session and message.content.startswith(POLL_PREFIX):
                # count_votes
                session.check_vote(message.content.upper(), message.author)

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
        self.voted = []

    def check_vote(self, message, author):
        vote = message.replace('?', '').split(' ')[0]
        # refactor
        if author.id not in self.voted and vote in self.choices.keys():
            self.voted.append(author.id)
            self.choices[vote] += 1

    @staticmethod
    def _convert(lst) -> dict:
        choices = {}
        for item in lst:
            choices[item] = 0

        return choices

    def poll_results(self) -> str:
        msg = 'Poll Results:\n'
        for k, v in self.choices.items():
            msg += f'{k}: {v}\n'
        return msg


def setup(bot):
    bot.add_cog(Poll(bot))
