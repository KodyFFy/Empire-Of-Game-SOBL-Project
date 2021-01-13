import re
import random
import asyncio

import discord
from discord.ext import commands
from util import GetMessage

time_regex = re.compile(r"(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}

def convert(argument):
	args = argument.lower()
	matches = re.findall(time_regex, args)
	time = 0
	for key, value in matches:
		try:
			time += time_dict[value] * float(key)
		except KeyError:
			raise commands.BadArgument(
				f"{value} is an invalid time key! h|m|s|d are valid arguments"
			)
		except ValueError:
			raise commands.BadArgument(f"{key} не число!")
	return round(time)



class Events(BOT.Cog):
	def __init__(self, bot):
		self.bot = bot



def setup(bot):
	bot.add_cog(Events(bot))