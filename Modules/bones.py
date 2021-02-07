import json
import random
import asyncio

import discord
from discord.ext import commands as BOT

from Imports.bin import info
import Modules.economy as econom


class Bones(BOT.Cog):
	def __init__(self, Bot):
		self.Bot = Bot

	@BOT.command()
	async def bones(self, ctx, num, amount=None):
		num = int(num)
		user = ctx.author
		await econom.open_account(user)
		users = await econom.get_main_data()
		# await ctx.send("Давайте бросим кубик! 🎲")
		# await ctx.send(file=discord.File("Images/Bones/bone_start.gif"))
		balance = int(users[str(user.id)]["Wallet"])

		if num > 6 or num == "" or num < 1:
			embed=discord.Embed(
				title="Ошибка!",
				description="Ошибка аргумента числа. Возможно вы ввели: отрицательное число / ничего / число больше 6 / число меньше 1 / текст",
				color=0xef3417)
			await ctx.send(embed=embed)

		else:
			if amount == None:
				ran = random.randint(1, 6)
				num = int(num)
				if num == ran:
					# name = "bone" +  "_" + str(ran) + ".gif"
					# await ctx.send(file=discord.File(f"Images/Bones/{name}"))
					embed=discord.Embed(
						title="Вы выиграли!",
						description=f"Кубик 🎲 упал и на нем число {ran}. Вы угадали поздравляю!",
						color=0x7289da)
					await ctx.send(embed=embed)

				else:
					# name = "bone" +  "_" + str(ran) + ".gif"
					# await ctx.send(file=discord.File(f"Images/Bones/{name}"))
					embed=discord.Embed(
						title="Вы проиграли!",
						description=f"Кубик 🎲 упал и на нем число {ran}. Увы вы не угадали :(")
					await ctx.send(embed=embed)

			else:
				if balance < int(amount):
					embed=discord.Embed(
						title="Ошибка!",
						description="У Вас нет столько денег для игры!",
						color=0xef3417)
					await ctx.send(embed=embed)

				else:
					num = int(num)
					user = ctx.author

					await econom.open_account(user)

					users = await econom.get_main_data()
					balance = int(users[str(user.id)]["Wallet"])
					reserv = int(amount)
					ran = random.randint(1, 6)

					if num == ran:
						# name = "bone" +  "_" + str(ran) + ".gif"
						# await ctx.send(file=discord.File(f"Images/Bones/{name}"))
						embed=discord.Embed(title="Вы выиграли!",
							description=f"Кубик 🎲 упал и на нем число {ran}. Вы угадали поздравляю! Ваш куш - {reserv + (reserv * 3.5)} <:coin:791004475098660904> ",
							color=0x7289da)
						await ctx.send(embed=embed)

						users[str(user.id)]["Wallet"] = int(
							users[str(user.id)]["Wallet"]) + int(reserv + (reserv * 3.5))

						with open("JSONs/main.json", "w") as f:
							json.dump(users, f, indent=4)

					else:
						# name = "bone" +  "_" + str(ran) + ".gif"
						# await ctx.send(file=discord.File(f"Images/Bones/{name}"))
						embed=discord.Embed(
							title="Вы проиграли!",
							description=f"Кубик 🎲 упал и на нем число {ran}. Увы вы не угадали :(")
						await ctx.send(embed=embed)

						users[str(user.id)]["Wallet"] = int(users[str(user.id)]["Wallet"]) - reserv

						with open("JSONs/main.json", "w") as f:
							json.dump(users, f, indent=4)


def setup(Bot):
	Bot.add_cog(Bones(Bot))
