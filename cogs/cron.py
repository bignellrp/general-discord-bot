from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ProcessPoolExecutor
from datetime import timedelta
from discord.ext import commands
import aiocron
from services.get_rate import check_for_negative_rates, get_optimal_time
from bot import bot, CHANNEL_ID

class Cron(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler()

    @aiocron.crontab('00 20 * * *')
    @commands.Cog.listener()
    async def cronmsg():
        get_channelid = int(CHANNEL_ID)
        channel = bot.get_channel(get_channelid)
        if check_for_negative_rates():
            await channel.send('Next 24hrs has negative rates!')

    @aiocron.crontab('20 13 * * *')
    @commands.Cog.listener()
    async def on_ready(self):
        optimal_period_start_time = get_optimal_time()
        optimal_period_start_time = optimal_period_start_time - timedelta(hours=4.5)
        if optimal_period_start_time:
            # Convert datetime to string format required by apscheduler - "%Y-%m-%d %H:%M:%S"
            str_optimal_time = optimal_period_start_time.strftime("%Y-%m-%d %H:%M:%S")
            
            self.scheduler.add_job(self.cronmsg, 'date', run_date=str_optimal_time)
            self.scheduler.start()

def setup(bot):
    bot.add_cog(Cron(bot))