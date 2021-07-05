import discord
from discord.ext import commands as BOT

from config import info


BLANK = "BLANK"

pos_1 = 0
pos_2 = 1
pos_3 = 2
pos_4 = 3
pos_5 = 4
pos_6 = 5
pos_7 = 6
pos_8 = 7
pos_9 = 8

react = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "❗️"]


class TickTakToe(BOT.Cog):
	def __init__(self, Bot):
		self.Bot = Bot


	@BOT.command()
	async def ttt(self, ctx, member: discord.Member = None):
		emoji = ["1️⃣", "2️⃣", "3️⃣",
				 "4️⃣", "5️⃣", "6️⃣",
				 "7️⃣", "8️⃣", "9️⃣", "❗️"
				]

		board = [BLANK, BLANK, BLANK,
				 BLANK, BLANK, BLANK,
				 BLANK, BLANK, BLANK
				]


		currentPlayer = 1
		
		player_1 =	await getUserChar(ctx,bot, currentPlayer)
		player_2 =	await getUserChar(ctx,bot, currentPlayer + 1)

		await ctx.channel.purge(limit = 3)

		def checkNooBot(reaction, user):
			return user != self.Bot

		while 

def setup(Bot):
	Bot.add_cog(TickTakToe(Bot))
