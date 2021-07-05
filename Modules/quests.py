import json
import random
import asyncio

import discord
from discord.ext import commands as BOT

from config import info
import Modules.economy as econom


class Quests(BOT.Cog):
	def __init__(self, Bot):
		self.Bot = Bot

	@BOT.command()
	async def expression(self, ctx, money):
		user = ctx.author
		await econom.open_account(user)
		kof = 0
		users = await econom.get_main_data()
		balance = int(users[str(user.id)]["Wallet"])
		new_money = money
		users[str(user.id)]["Wallet"] -= int(money)
		with open("JSONs/main.json", "w") as f:
			json.dump(users, f, indent=2)
		if int(money) > int(balance):
			await ctx.send("У вас нет столько <:coin:791004475098660904> 😈!")

		else:
			guild = ctx.guild
			player = ctx.author.name
			name = player + " " + " game"

			perms = {
				guild.me: discord.PermissionOverwrite(
					read_messages=True,
					send_messages=True
				),

				ctx.author: discord.PermissionOverwrite(
					read_messages=True,
					send_messages=True
				),

				guild.default_role: discord.PermissionOverwrite(
					read_messages=False
				)
				}
			id_cat = 810970353261871134
			channel = await ctx.guild.create_text_channel(
				name=f"{name}",
				overwrites=perms,
				category=self.Bot.get_channel(id_cat) ### id_cat --- ID категории
			)

			timeout_0 = 120
			embed = discord.Embed(
				title="||@here||. Для начала игры напишите **start** в чат. Если вы передумали, напишите **stop**. Если не будет ответа канал удалится черещ 2 минуты",
				color=0x7289da
			)
			await channel.send(embed=embed)

			try:
				user_answ = await self.Bot.wait_for(
					"message",
					timeout=timeout_0,
					check=lambda message: message.author == ctx.author and message.channel == channel
				)

			except asyncio.TimeoutError:
				await channel.delete()
				users[str(user.id)]["Wallet"] += int(money)

				with open("JSONs/main.json", "w") as f:
					json.dump(users, f, indent=2)
			else:
				if user_answ.content == "start":
					embed = discord.Embed(
						title="Начинаем!",
						description="",
						color=0x7289da
					)
					await channel.send(embed=embed)

					
					timeout = 8     ### seconds
					while True:
						symbols = ["+", "-"]

						num1 = random.randint(1, 150)
						num2 = random.randint(1, 150)

						_symbols = random.choice(symbols)

						math = str(num1) + " " + _symbols + " " + str(num2)
						await channel.send(math)
						answ = 0

						if _symbols == "+":
							answ = num1 + num2
							print(answ)

						elif _symbols == "-":
							answ = num1 - num2
							print(answ)

						try:
							user_answ = await self.Bot.wait_for(
								"message",
								timeout=timeout,
								check=lambda message: message.author == ctx.author and message.channel == channel
							)

						except asyncio.TimeoutError:
							await channel.send("Время вышло! Игра завершина!")
							break

						else:
							try:
								if int(user_answ.content) == int(answ):
									kof += 1
									new_money = (float(new_money) * 0.02 * float(kof))
									ger = round(int(new_money), 0)
									await channel.send(
										f"Верно! Идем дальше. Правльных ответов: {kof}, Ваш выйгрыш: {ger}"
									)

								elif user_answ != answ or user_answ == None:
									embed = discord.Embed(
										title="Ответ неверный!"
									)
									await channel.send(embed=embed)
									break

							except:
								await channel.send("Произошла Ошибка! Игра аврийно завершина!")
								break


					new_money = (float(new_money) * 0.25 * float(kof))
					ger = round(int(new_money), 0)
					embed = discord.Embed(
						title="Игра окончена!",
						description="Подсчитываю резултьтаты..."
					)
					await channel.send(embed=embed)

					await asyncio.sleep(2)

					embed = discord.Embed(
						title="Результаты",
						description=f"Вы ответили правильно на {kof} примеров.\n Ваша ставка превратилась в {ger} <:coin:791004475098660904>"
					)
					await channel.send(embed=embed)

					users[str(user.id)]["Wallet"] += int(ger)

					with open("JSONs/main.json", "w") as f:
						json.dump(users, f, indent=2)

					await channel.send(
						"Проверьте свой баланс, если что-то не так сделайте скрин.\nНа все у вас есть 30 секунд. После канал **самоуничтожится!**"
					)
					await asyncio.sleep(30)
					await channel.delete()

				elif user_answ.content.lower() == "stop":
					await channel.send(
						"Мы вернули вашу ставку!. Через 5 секунд канал **самоуничтожится!**"
					)
					users[str(user.id)]["Wallet"] += int(money)

					with open("JSONs/main.json", "w") as f:
						json.dump(users, f, indent=2)

					await asyncio.sleep(5)
					await channel.delete()

				else:
					await channel.send("Неизвестная комманда! Завершаю игру!")
					await channel.send(
 						"Мы вернули вашу ставку!. Через 5 секунд канал **самоуничтожится!**"
 					)
					users[str(user.id)]["Wallet"] += int(money)

					with open("JSONs/main.json", "w") as f:
						json.dump(users, f, indent=2)

					await asyncio.sleep(5)
					await channel.delete()

def setup(Bot):
	Bot.add_cog(Quests(Bot))