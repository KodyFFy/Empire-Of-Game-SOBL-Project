import json
import random

import discord
from discord.ext import commands as BOT

from config import info
import Modules.economy as econom



class Flip(BOT.Cog):
	def __init__(self, Bot):
		self.Bot = Bot

	@BOT.command()
	async def flip(self, ctx, oborot ,amount = None):
		user = ctx.author
		await econom.open_account(user)

		users = await econom.get_main_data()	
		balance = int(users[str(user.id)]["Wallet"])
		oborot = oborot.lower()
		if oborot == "орел":
			rand = random.randint(0, 1) # 0 - Орел; 1 - Решка;
			if amount == None:
				if rand == 0:
					embed=discord.Embed(
						title="Вы выиграли!",
						description="Фортуна улыбается вам! Вы угадали!",
						color=0x7289da)
					await ctx.send(embed=embed)

				else:
					embed=discord.Embed(
						title="Вы проиграли!",
						description="Рандом послал вас. Вы проиграли!",
						color=0x7289da)
					await ctx.send(embed=embed)

			else:
				if balance < int(amount):
					embed=discord.Embed(
						title="Ошибка!",
						description="У Вас нет столько денег для игры!",
						color=0xef3417)
					await ctx.send(embed=embed)

				else:
					reserv = int(amount)

					if rand == 0:
						embed=discord.Embed(
							title="Вы выиграли!",
							description=f"Фортуна улыбается вам! Вы угадали! Выигрыш - {reserv + (reserv * 1//6)} <:coin:791004475098660904>",
							color=0x7289da)
						await ctx.send(embed=embed)

						users[str(user.id)]["Wallet"] = int(users[str(user.id)]["Wallet"]) + int(reserv + (reserv * 1//6))
						
						with open("JSONs/main.json", "w") as f:
							json.dump(users, f, indent = 3)

					else:
						embed=discord.Embed(
							title="Вы проиграли!",
							description="Рандом послал вас. Вы проиграли!",
							color=0x7289da)
						await ctx.send(embed=embed)

						users[str(user.id)]["Wallet"]  = int(users[str(user.id)]["Wallet"]) - reserv
						
						with open("JSONs/main.json", "w") as f:
							json.dump(users, f, indent = 3)

		elif oborot == "решка":
			rand = random.randint(0,1) # 1 - Орел; 0 - Решка;
			if amount == None:
				if rand == 0:
					embed=discord.Embed(
						title="Вы выиграли!",
						description="Фортуна улыбается вам! Вы угадали!",
						color=0x7289da)
					await ctx.send(embed=embed)

				else:
					embed=discord.Embed(
						title="Вы проиграли!",
						description="Рандом послал вас. Вы проиграли!",
						color=0x7289da)
					await ctx.send(embed=embed)

			else:
				if balance < int(amount):
					embed=discord.Embed(
						title="Ошибка!",
						description="У Вас нет столько денег для игры!",
						color=0xef3417)
					await ctx.send(embed=embed)
				
				else:
					reserv = int(amount)

					if rand == 0:
						embed=discord.Embed(
							title="Вы выиграли!",
							description=f"Фортуна улыбается вам! Вы угадали! Выигрыш - {reserv + (reserv * 1//6)} <:coin:791004475098660904>",
							color=0x7289da)
						await ctx.send(embed=embed)

						users[str(user.id)]["Wallet"]  = int(users[str(user.id)]["Wallet"]) + (reserv + (reserv * 1//6))
				
					else:
						await ctx.send("Рандом послал вас. Вы проиграли!")
						users[str(user.id)]["Wallet"]  = int(users[str(user.id)]["Wallet"]) - reserv
					
					with open("JSONs/main.json", "w") as f:
						json.dump(users, f, indent = 3)

		else:
			await ctx.send("Вы не ввели Орел или Решка или вы ошиблись в слове. Попробуйте снова!")


def setup(Bot):
	Bot.add_cog(Flip(Bot))
