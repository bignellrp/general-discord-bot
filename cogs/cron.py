from discord.ext import commands
import aiocron
from bot import CHANNEL_ID
from services.get_rate import check_for_negative_rates

class Cron(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @aiocron.crontab('30 19 * * *')
    @commands.Cog.listener()
    async def cronmsg(self):
        get_channelid = int(CHANNEL_ID)
        channel = self.bot.get_channel(get_channelid)
        if check_for_negative_rates():
            await channel.send('Next 24hrs has negative rates!')

def setup(bot):
    bot.add_cog(Cron(bot))