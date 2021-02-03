import json
import random
import asyncio

import discord
from discord.ext import commands as BOT

from Imports.bin import info
import Modules.economy as econom

# botPrefix = info[""]

wait_bonus = []
class Bonus(BOT.Cog):
	def __init__(self, Bot):
		self.Bot = Bot

	@BOT.command()
	async def bonus(self, ctx):
		await ctx.send("Для получения бонуса перейдите по ссылке и разрешите уведомление! Потом пропишите {pref}use (код)")
		await ctx.send("Нажимая разрешить уведомления при переходе, вы помогаете серверу")
		await ctx.send("Ссылка >>> https://goo.su/EOG_PROMO")
		await ctx.send("Документация по удалению уведомления из вашего браузера >>> https://goo.su/41kZ")

	@BOT.command()
	async def create_promo(self,ctx,promo_cod, activ):
		with open('JSONs/promos.json', 'r') as f:
			promos = json.load(f)

		if str(promo_cod) in promos:
			await ctx.send(f"Такой промокод уже есть, чтобы изменить его удалите его и снова создайте. Вы можете узнать о промокодах и инфу о них с помощью {pref}listpromo")

		else:
			if int(activ) == 0:
					await ctx.send("Промокод с бесконечным количеством использования, успешно создан!")
					promo_cod = str(promo_cod)
					with open('JSONs/promos.json','r') as f:
						promos = json.load(f)

						promos[promo_cod] = {}
						promos[promo_cod][promo_cod] = promo_cod
						promos[promo_cod][promo_cod] = {}
						promos[promo_cod][promo_cod]['Options'] = {}
						promos[promo_cod][promo_cod]['Options']['Use'] = activ

			elif int(activ) < 0:
				await ctx.send("Количество активаций должно быть неотрицательным **числом**")

			else:
					await ctx.send(f"Промокод c {activ} использованиями, успешно создан!")
					promo_cod = str(promo_cod)
					with open('JSONs/promos.json','r') as f:
						promos = json.load(f)

						promos[promo_cod] = {}
						promos[promo_cod][promo_cod] = promo_cod
						promos[promo_cod][promo_cod] = {}
						promos[promo_cod][promo_cod]['Options'] = {}
						promos[promo_cod][promo_cod]['Options']['Use'] = activ
		with open('JSONs/promos.json', 'w') as f:
			json.dump(promos,f, indent=3)

	@BOT.command()
	async def del_promo(self,ctx, promo_cod):
		with open('JSONs/promos.json', 'r') as f:
			promos = json.load(f)
	
		if str(promo_cod) in promos:
			del promos[promo_cod]
			await ctx.send("Прмокод успешно удален!")
			with open('JSONs/promos.json', 'w') as f:
				json.dump(promos, f, indent=3)
		else:
			await ctx.send("Такого промокода нет или вы неправильно его указали!")

	@BOT.command()
	async def listpromo(self,ctx):
		with open('JSONs/promos.json', 'r') as f:
			promos = json.load(f)

		embed = discord.Embed(
			title="Все промокоды",
			color=0x8cff1a)
		
		for i in promos:
			name = i
			
			activ = promos[i][i]['Options']['Use']
			embed.add_field(
				name=f"Промокод ---> {i}",
				value=f"Количество использований ---> {activ}, Если количество использований 0, то неограниченно",
				inline=False)
		await ctx.send("Инфа о промокодах", embed=embed)


	@BOT.command()
	async def use(self,ctx, promo):
		with open('JSONs/promos.json', 'r') as f:
			promos = json.load(f)

		if not str(ctx.author.id) in wait_bonus:
			for i in promos:
				if promo == i:
					aciv = promos[i][i]['Options']['Use']
					if aciv == 0:
						user = ctx.author
						await econom.open_account(user)

						users = await econom.get_main_data()	
						balance = int(users[str(user.id)]["Bank"])

						get = random.randint(250, 4500)

						users[str(user.id)]["Bank"] += get

						await ctx.send("Промокод успешно активирован!")
						with open("JSONs/main.json", "w") as f:
							json.dump(users, f, indent=3)
						wait_bonus.append(str(ctx.author.id))

					elif aciv == 1:

						promos[i][i]['Options']['Use'] = -1
						user = ctx.author
						await econom.open_account(user)

						users = await econom.get_main_data()	
						balance = int(users[str(user.id)]["Bank"])

						get = random.randint(250, 4500)

						users[str(user.id)]["Bank"] += get
						await ctx.send("Промокод успешно активирован!")
						with open("JSONs/main.json", "w") as f:
							json.dump(users, f, indent=3)
						wait_bonus.append(str(ctx.author.id))

					elif aciv == -1:
						await ctx.send("Промокод истек :(")

					else:
						aciv = int(promos[i][i]['Options']['Use'])
						aciv -= 1
						promos[i][i]['Options']['Use'] = aciv
						user = ctx.author
						await econom.open_account(user)

						users = await econom.get_main_data()	
						balance = int(users[str(user.id)]["Bank"])

						get = random.randint(250, 4500)

						users[str(user.id)]["Bank"] += get
						await ctx.send("Промокод успешно активирован!")
						with open("JSONs/main.json", "w") as f:
							json.dump(users, f, indent=3)
						wait_bonus.append(str(ctx.author.id))
			if not promo in promos:
				await ctx.send("Такого промокода нет :(")

			with open('JSONs/promos.json','w') as f:
				json.dump(promos,f, indent=3)
			await asyncio.sleep(24*60*60)
			wait_beg.remove(str(ctx.author.id))

		else:
			await ctx.send("Вы сегодня уже использовали промокод! Приходите завтра!")

def setup(Bot):
	Bot.add_cog(Bonus(Bot))
