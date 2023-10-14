from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ProcessPoolExecutor
from datetime import timedelta
from discord.ext import commands
import aiocron
from services.get_rate import check_for_negative_rates, get_optimal_time
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

    @aiocron.crontab('45 13 * * *')
    @commands.Cog.listener()
    async def set_schedule():
        optimal_period_start_time = get_optimal_time()
        optimal_period_start_time = optimal_period_start_time - timedelta(hours=4.5)
        get_channelid = int(CHANNEL_ID)
        channel = bot.get_channel(get_channelid)
        if optimal_period_start_time:
            # Convert datetime to string format required by apscheduler - "%Y-%m-%d %H:%M:%S"
            str_optimal_time = optimal_period_start_time.strftime("%Y-%m-%d %H:%M:%S")
            # Create message ready to run on a schedule
            msg = await channel.send(f'Schedule set to run at {str_optimal_time}')
            
            scheduler.add_job(msg, 'date', run_date=str_optimal_time)
            scheduler.start()

def setup(bot):
    bot.add_cog(Cron(bot))