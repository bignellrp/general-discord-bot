import discord
from discord.ext import commands
from services.get_rate import get_rate, get_avg_rate
from services.smart_plug import control_smart_plug
from services.get_rate import *
from bot import bot, CHANNEL_ID, scheduler
from datetime import timedelta, datetime

class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rate(self, ctx, member: discord.Member = None):
        """Get Octopus Agile rate"""
        file = discord.File("static/octopus.png")
        member = member or ctx.author
        get_rate_value = get_rate()
        get_rate_value = str(get_rate_value) + "p/kWh"
        ##Embed Message
        embed=discord.Embed(
            title="Current Octopus Rate",
            description=get_rate_value,
            color=discord.Color.green()
        )
        embed.set_thumbnail(url="attachment://octopus.png")
        print("Posted Current Rate to Discord!")
        await ctx.send(file=file, embed=embed)

    @commands.command()
    async def avg(self, ctx, member: discord.Member = None):
        """Get Octopus Agile avg rate"""
        file = discord.File("static/octopus.png")
        member = member or ctx.author
        get_rate_value = get_avg_rate()
        get_rate_value = str(get_rate_value) + "p/kWh"
        ##Embed Message
        embed=discord.Embed(
            title="Octopus Avg Rate for 12hrs",
            description=get_rate_value,
            color=discord.Color.green()
        )
        embed.set_thumbnail(url="attachment://octopus.png")
        print("Posted Current Rate to Discord!")
        await ctx.send(file=file, embed=embed)

    @commands.command()
    async def on(self, ctx, member: discord.Member = None):
        """Turn plug on manually"""
        member = member or ctx.author
        control_smart_plug("on")
        print("Manually turned plug on!")

    @commands.command()
    async def off(self, ctx, member: discord.Member = None):
        """Turn plug off manually"""
        member = member or ctx.author
        control_smart_plug("off")
        print("Manually turned plug off!")

    @commands.command()
    async def set(self, ctx, member: discord.Member = None):
        """Manually override schedule"""
        member = member or ctx.author
        get_channelid = int(CHANNEL_ID)
        channel = bot.get_channel(get_channelid)
        optimal_period_end_time, average = get_optimal_time()
        optimal_period_start_time = optimal_period_end_time - timedelta(hours=5)
        start_time = optimal_period_start_time.strftime("%Y-%m-%d %H:%M:%S")
        end_time = optimal_period_end_time.strftime("%Y-%m-%d %H:%M:%S")

        if start_time > datetime.now():
            scheduler.remove_all_jobs()
            await channel.send(f'Schedule set to start at {start_time} with average of {average}p/kwh')
            scheduler.add_job(control_smart_plug, 'date', run_date=start_time, args=["on"])
            scheduler.add_job(control_smart_plug, 'date', run_date=end_time, args=["off"])
            scheduler.start()
        else:
            await channel.send('Error setting schedule!')

    @commands.command()
    async def set12(self, ctx, member: discord.Member = None):
        """Manually override schedule"""
        member = member or ctx.author
        get_channelid = int(CHANNEL_ID)
        channel = bot.get_channel(get_channelid)
        optimal_period_end_time, average = get_optimal_time12()
        optimal_period_start_time = optimal_period_end_time - timedelta(hours=5)
        start_time = optimal_period_start_time.strftime("%Y-%m-%d %H:%M:%S")
        end_time = optimal_period_end_time.strftime("%Y-%m-%d %H:%M:%S")

        if start_time > datetime.now():
            scheduler.remove_all_jobs()
            await channel.send(f'Schedule set to start at {start_time} with average of {average}p/kwh')
            scheduler.add_job(control_smart_plug, 'date', run_date=start_time, args=["on"])
            scheduler.add_job(control_smart_plug, 'date', run_date=end_time, args=["off"])
            scheduler.start()
        else:
            await channel.send('Error setting schedule!')

    @commands.command()
    async def set24(self, ctx, member: discord.Member = None):
        """Manually override schedule"""
        member = member or ctx.author
        get_channelid = int(CHANNEL_ID)
        channel = bot.get_channel(get_channelid)
        optimal_period_end_time, average = get_optimal_time24()
        optimal_period_start_time = optimal_period_end_time - timedelta(hours=5)
        start_time = optimal_period_start_time.strftime("%Y-%m-%d %H:%M:%S")
        end_time = optimal_period_end_time.strftime("%Y-%m-%d %H:%M:%S")

        if start_time > datetime.now():
            scheduler.remove_all_jobs()
            await channel.send(f'Schedule set to start at {start_time} with average of {average}p/kwh')
            scheduler.add_job(control_smart_plug, 'date', run_date=start_time, args=["on"])
            scheduler.add_job(control_smart_plug, 'date', run_date=end_time, args=["off"])
            scheduler.start()
        else:
            await channel.send('Error setting schedule!')

    @commands.command()
    async def can(self, ctx, member: discord.Member = None):
        """Cancel schedule"""
        member = member or ctx.author
        scheduler.remove_all_jobs()
        await ctx.send(f'Schedule cancelled!')

def setup(bot):
    bot.add_cog(Commands(bot))