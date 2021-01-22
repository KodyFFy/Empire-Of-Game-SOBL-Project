import discord
from discord.ext import commands as BOT
import json
import random
import asyncio
from Imports.bin import info

import Modules.economy as econom


class Bones(BOT.Cog):
	def __init__(self, Bot):
		self.Bot = Bot

	@BOT.command()
	async def bones(self, ctx, num ,amount = None):
		num = int(num)
		user = ctx.author
		await econom.open_account(user)
		users = await econom.get_main_data()	
		#await ctx.send("Давайте бросим кубик! 🎲")
		#await ctx.send(file=discord.File('imgs/bones/bone_start.gif'))
		balance = int(users[str(user.id)]['Wallet'])

		if num > 6 or num == "" or num < 1:
			await ctx.send("Ошибка аргумента числа. Возможно вы ввели: отрицательное число / ничего / число больше 6 / число меньше 1 / текст")
		
		else:
			if amount == None:

				ran = random.randint(1,6)
				num = int(num)
				if num == ran:
					#name = "bone" +  "_" + str(ran) + ".gif"
					#await ctx.send(file=discord.File(f'imgs/bones/{name}'))
					await ctx.send(f"Кубик 🎲 упал и на нем число {ran}. Вы угадали поздравляю!")
				else:
					#name = "bone" +  "_" + str(ran) + ".gif"
					#await ctx.send(file=discord.File(f'imgs/bones/{name}'))
					await ctx.send(f"Кубик 🎲 упал и на нем число {ran}. Увы вы не угадали :(")

			else:
				if balance < int(amount):
					await ctx.send("У тебя нет столько денег для игры")

				else:
					num = int(num)
					user = ctx.author

					await econom.open_account(user)

					users = await econom.get_main_data()	

					balance = int(users[str(user.id)]['Wallet'])

					reserv = int(amount)

					ran = random.randint(1,6)

					if num == ran:
						#name = "bone" +  "_" + str(ran) + ".gif"
						#await ctx.send(file=discord.File(f'imgs/bones/{name}'))

						await ctx.send(f"Кубик 🎲 упал и на нем число {ran}. Вы угадали поздравляю! Ваш куш - {reserv + (reserv * 3.5)} <:coin:791004475098660904> ")

						users[str(user.id)]['Wallet'] = int(users[str(user.id)]['Wallet']) + int(reserv + (reserv * 3.5))
						
						with open('JSONs/main.json', 'w') as f:
							json.dump(users, f, indent = 3)

					else:
						#name = "bone" +  "_" + str(ran) + ".gif"
						#await ctx.send(file=discord.File(f'imgs/bones/{name}'))
						await ctx.send(f"Кубик 🎲 упал и на нем число {ran}. Увы вы не угадали :(")
						users[str(user.id)]['Wallet']  = int(users[str(user.id)]['Wallet']) - reserv
						
						with open('JSONs/main.json', 'w') as f:
							json.dump(users, f, indent = 3)

def setup(Bot):
	Bot.add_cog(Bones(Bot))