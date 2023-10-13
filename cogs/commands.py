import discord
from discord.ext import commands
from services.get_rate import get_rate, get_avg_rate

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

def setup(bot):
    bot.add_cog(Commands(bot))