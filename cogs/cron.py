from discord.ext import commands
import aiocron
from bot import bot, CHANNEL_ID
from services.get_rate import check_for_negative_rates

class Cron(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @aiocron.crontab('00 19 * * *')
    @commands.Cog.listener()
    async def cronmsg():
        get_channelid = int(CHANNEL_ID) #The chnnelid must be an int
        channel = bot.get_channel(get_channelid) #Should not be hardcoded
        if check_for_negative_rates():
            await channel.send('Next 24hrs has negative rates!')

def setup(bot):
    bot.add_cog(Cron(bot))