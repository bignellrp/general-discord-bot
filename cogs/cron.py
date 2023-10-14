from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ProcessPoolExecutor
from datetime import timedelta
from discord.ext import commands
import aiocron
from services.get_rate import check_for_negative_rates, get_optimal_time
from services.smart_plug import control_smart_plug
from bot import bot, CHANNEL_ID

scheduler = AsyncIOScheduler()

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

    @aiocron.crontab('50 15 * * *')
    @commands.Cog.listener()
    async def set_schedule():
        optimal_period_end_time = get_optimal_time()
        optimal_period_start_time = optimal_period_end_time - timedelta(hours=6)
        start_time = optimal_period_start_time.strftime("%Y-%m-%d %H:%M:%S")
        end_time = optimal_period_end_time.strftime("%Y-%m-%d %H:%M:%S")
        get_channelid = int(CHANNEL_ID)
        channel = bot.get_channel(get_channelid)
        if start_time:
            await channel.send(f'Schedule set to run at {start_time}')
            scheduler.add_job(control_smart_plug("on"), 'date', run_date=start_time)
            scheduler.add_job(control_smart_plug("off"), 'date', run_date=end_time)
            scheduler.start()

def setup(bot):
    bot.add_cog(Cron(bot))