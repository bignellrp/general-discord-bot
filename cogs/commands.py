import discord
from discord.ext import commands
from services.get_newrate import get_rate, get_avg_rate, get_min_avg_rate
from services.smart_plug import control_smart_plug
from services.get_rate import *
from bot import bot, CHANNEL_ID, scheduler, USER, PASSWORD, HOST
from datetime import datetime
import os
import paramiko

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
    async def book(self, ctx, *, numbers: str):
        """Book days by specifying numbers between 0 and 6"""
        # Validate the input
        if not numbers.isdigit() or any(char not in "0123456" for char in numbers):
            await ctx.send("Invalid input! Please provide a string of numbers between 0 and 6, e.g., 025.")
            return

        # Create the `days` file with the numbers
        file_path = "days"
        with open(file_path, "w") as file:
            file.write(numbers)

        # SCP the file to the remote location using paramiko
        remote_user = USER
        remote_host = HOST
        remote_path = f"/home/{USER}/unityplace-carpark/days"
        password = PASSWORD

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(remote_host, username=remote_user, password=password)

            sftp = ssh.open_sftp()
            sftp.put(file_path, remote_path)
            sftp.close()
            ssh.close()

            await ctx.send(f"{numbers} days file successfully sent to {remote_user}@{remote_host}:{remote_path}")
        except Exception as e:
            await ctx.send("Failed to transfer the file via SCP. Please check your configuration.")
            print(f"SCP error: {e}")

        # Clean up the local file
        os.remove(file_path)

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
        #optimal_period_end_time, average = get_optimal_time()
        #optimal_period_start_time = optimal_period_end_time - timedelta(hours=5)
        optimal_period_start_time, optimal_period_end_time, average = get_min_avg_rate()
        start_time = optimal_period_start_time.strftime("%Y-%m-%d %H:%M:%S")
        end_time = optimal_period_end_time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Code assumes start_time is a string in this format: '%Y-%m-%d %H:%M:%S'
        parsed_start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')

        if start_time and parsed_start_time > datetime.now():
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

    @commands.command()
    async def show(self, ctx):
        """Show current schedule"""
        if not scheduler.get_jobs():
            await ctx.send("No scheduled jobs.")
        else:
            response = "Current Jobs:\n"
            for job in scheduler.get_jobs():
                response += f"Job ID: {job.id}, next run at: {job.next_run_time}\n"
            await ctx.send(response)

def setup(bot):
    bot.add_cog(Commands(bot))