# from discord.ext import commands
# import aiocron
# from bot import bot, CHANNEL_ID

# class Cron(commands.Cog):

#     def __init__(self, bot):
#         self.bot = bot

#     @aiocron.crontab('00 09 * * SUN')
#     @commands.Cog.listener()
#     async def cronmsg():
#         get_channelid = int(CHANNEL_ID) #The chnnelid must be an int
#         channel = bot.get_channel(get_channelid) #Should not be hardcoded
#         await channel.send('Cron message!!!!')

# def setup(bot):
#     bot.add_cog(Cron(bot))