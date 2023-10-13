from discord.ext import commands
import aiocron
from services.get_rate import check_for_negative_rates
from bot import bot, CHANNEL_ID

class Cron(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @aiocron.crontab('00 20 * * *')
    @commands.Cog.listener()
    async def cronmsg():
        get_channelid = int(CHANNEL_ID)
        channel = bot.get_channel(get_channelid)
        if check_for_negative_rates():
            await channel.send('Next 24hrs has negative rates!')

def setup(bot):
    bot.add_cog(Cron(bot))