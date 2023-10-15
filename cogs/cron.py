from datetime import timedelta
from discord.ext import commands
import aiocron
from services.get_rate import *
from services.smart_plug import control_smart_plug
from bot import bot, CHANNEL_ID, scheduler

class Cron(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @aiocron.crontab('00 20 * * *')
    @commands.Cog.listener()
    async def set_schedule():
        get_channelid = int(CHANNEL_ID)
        channel = bot.get_channel(get_channelid)
        optimal_period_end_time, average = get_optimal_time24()
        optimal_period_start_time = optimal_period_end_time - timedelta(hours=5)
        start_time = optimal_period_start_time.strftime("%Y-%m-%d %H:%M:%S")
        end_time = optimal_period_end_time.strftime("%Y-%m-%d %H:%M:%S")
        if check_for_negative_rates():
            await channel.send('Next 24hrs has negative rates!')
        
        # Here we remove all other jobs first
        scheduler.remove_all_jobs()

        if start_time:
            await channel.send(f'Schedule set to start at {start_time} with average of {average}p/kwh')
            scheduler.add_job(control_smart_plug, 'date', run_date=start_time, args=["on"])
            scheduler.add_job(control_smart_plug, 'date', run_date=end_time, args=["off"])
            scheduler.start()

def setup(bot):
    bot.add_cog(Cron(bot))