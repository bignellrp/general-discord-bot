import discord
from discord.ext import commands
from services.get_rate import get_rate, get_avg_rate
from services.smart_plug import control_smart_plug
from services.get_rate import get_optimal_time
from bot import bot, CHANNEL_ID, scheduler
from datetime import timedelta

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
        """Get Octopus Agile average rate"""
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
        """Manually override the schedule"""
        member = member or ctx.author
        optimal_period_end_time = get_optimal_time()
        optimal_period_start_time = optimal_period_end_time - timedelta(hours=5)
        start_time = optimal_period_start_time.strftime("%Y-%m-%d %H:%M:%S")
        end_time = optimal_period_end_time.strftime("%Y-%m-%d %H:%M:%S")
        get_channelid = int(CHANNEL_ID)
        channel = bot.get_channel(get_channelid)

        # Here we remove all other jobs first
        scheduler.remove_all_jobs()

        if start_time:
            await channel.send(f'Schedule set to run at {start_time}')
            scheduler.add_job(control_smart_plug("on"), 'date', run_date=start_time)
            scheduler.add_job(control_smart_plug("off"), 'date', run_date=end_time)
            scheduler.start()

def setup(bot):
    bot.add_cog(Commands(bot))