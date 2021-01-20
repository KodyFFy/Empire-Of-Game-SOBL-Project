import discord
from discord.ext import commands as BOT
import json
import random
import asyncio
from Imports.bin import info

import Modules.economy as econom



class Flip(BOT.Cog):
	def __init__(self, Bot):
		self.Bot = Bot

	@BOT.command()
	async def flip(self, ctx, oborot ,amount = None):



		user = ctx.author

		await econom.open_account(user)

		users = await econom.get_main_data()	

		balance = int(users[str(user.id)]['Wallet'])
		print(balance)


		if oborot == "Орел":

			rand = random.randint(0, 1) # 0 - Орел; 1 - Решка;

			if amount == None:
				
				if rand == 0:
					await ctx.send("Фортуна улыбается вам! Вы угадали!")

				else:
					await ctx.send("Рандом послал вас. Вы проиграли!")

			else:
				if balance < int(amount):
					await ctx.send("У тебя нет столько денег для игры")

				else:
					reserv = int(amount)

					if rand == 0:
						await ctx.send(f"Фортуна улыбается вам! Вы угадали! Выигрыш - {reserv + (reserv * 0.5)}")
						users[str(user.id)]['Wallet'] = int(users[str(user.id)]['Wallet']) + int(reserv + (reserv * 0.5))
						with open('main.json', 'w') as f:
							json.dump(users, f, indent = 3)

					else:
						await ctx.send("Рандом послал вас. Вы проиграли!")
						users[str(user.id)]['Wallet']  = int(users[str(user.id)]['Wallet']) - reserv
						with open('main.json', 'w') as f:
							json.dump(users, f, indent = 3)

		elif oborot == "Решка":

			rand = random.randint(0,1) # 1 - Орел; 0 - Решка;

			if amount == None:
				
				if rand == 0:
					await ctx.send("Фортуна улыбается вам! Вы угадали!")

				else:
					await ctx.send("Рандом послал вас. Вы проиграли!")

			else:
				if balance < int(amount):
					await ctx.send("У тебя нет столько денег для игры")
				
				else:
					reserv = int(amount)

					if rand == 0:
						await ctx.send(f"Фортуна улыбается вам! Вы угадали! Фортуна улыбается вам! Вы угадали! Выигрыш - {reserv + (reserv * 0.5)}")
						users[str(user.id)]['Wallet']  = int(users[str(user.id)]['Wallet']) + (reserv + (reserv * 0.5))
				
					else:
						await ctx.send("Рандом послал вас. Вы проиграли!")
						users[str(user.id)]['Wallet']  = int(users[str(user.id)]['Wallet']) - reserv
					
					with open('main.json', 'w') as f:
						json.dump(users, f, indent = 3)

		else:
			await ctx.send("Вы не ввели Орел или Решка или вы ошиблись в слове. Попробуйте снова!")


def setup(Bot):
	Bot.add_cog(Flip(Bot))