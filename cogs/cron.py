from datetime import datetime, timedelta
from discord.ext import commands
import aiocron
from services.get_newrate import get_min_avg_rate, check_for_negative_rates
from services.smart_plug import control_smart_plug
#from services.book_carpark import bookcarpark
from bot import bot, CHANNEL_ID, scheduler

class Cron(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @aiocron.crontab('00 20 * * *')
    @commands.Cog.listener()
    async def set_schedule():
        get_channelid = int(CHANNEL_ID)
        channel = bot.get_channel(get_channelid)
        optimal_period_start_time, optimal_period_end_time, average = get_min_avg_rate()
        #optimal_period_end_time, average = get_optimal_time24()
        #optimal_period_start_time = optimal_period_end_time - timedelta(hours=5)
        start_time = optimal_period_start_time.strftime("%Y-%m-%d %H:%M:%S")
        end_time = optimal_period_end_time.strftime("%Y-%m-%d %H:%M:%S")
        if check_for_negative_rates():
            await channel.send('Next 24hrs has negative rates!')
        
        # Determine the day of the week for tomorrow
        tomorrow = datetime.now() + timedelta(days=1)
        day_of_week = tomorrow.weekday()  # Monday = 0, Tuesday = 1, ..., Sunday = 6
        # Set the time to 6:05 AM
        car_time = tomorrow.replace(hour=6, minute=5, second=0, microsecond=0)
        
        # Code assumes start_time is a string in this format: '%Y-%m-%d %H:%M:%S'
        parsed_start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')

        if start_time and parsed_start_time > datetime.now():
            scheduler.remove_all_jobs()
            await channel.send(f'Smartplug: Starts {start_time} at {average}p/kwh')
            scheduler.add_job(control_smart_plug, 'date', run_date=start_time, args=["on"])
            #if day_of_week in [6, 1, 2]:
            #    await channel.send(f'Carpark: Starts at 6:05am tomorrow')
            #    scheduler.add_job(bookcarpark, 'date', run_date=car_time)
            scheduler.add_job(control_smart_plug, 'date', run_date=end_time, args=["off"])
            scheduler.start()
        else:
            await channel.send('Error setting schedule!')

def setup(bot):
    bot.add_cog(Cron(bot))