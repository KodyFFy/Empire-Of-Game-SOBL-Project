import json
import discord
from discord.ext import commands
import random
from bin import info
import asyncio
#import datetime

pref = info['PREFIX']
Bot = commands.Bot( command_prefix = pref )
name_Shop_id = "Roles"




@Bot.event
async def on_ready():
	print("Бот успешно запущен!")
Bot.remove_command('help')


@Bot.event 
async def on_command_error(ctx,error):
	if isinstance(error, commands.MissingRequiredArgument):
		embed=discord.Embed(color=0xff0000)
		embed.add_field(name="Ошибка!",
						value="Неверный аргумент. Возможно была допущена ошибка при вводе, попробуй `e!help` что-бы узнать больше о команде.",
						inline=True
						)
		await ctx.send(embed=embed)

	if isinstance(error, commands.CommandNotFound):
		embed=discord.Embed(color=0xff0000)
		embed.add_field(name="Ошибка!", value="Такой команды не существует! Воспользуйся `e!help`!", inline=True)
		await ctx.send(embed=embed)


Bot.load_extension("Modules.help")
Bot.load_extension("Modules.economy")
Bot.load_extension("Modules.giveaway")


########################################################################################################
#
#mainshop = [{"name":"Watch","price":100,"description":"Time"},
#            {"name":"Laptop","price":1000,"description":"Work"},
#            {"name":"PC","price":10000,"description":"Gaming"}]
#
#
#@Bot.command() ### Вывыод окна магазина
#async def shop(ctx): 
#    em = discord.Embed(title = "Магазин")
#   for item in mainshop:
#   	name = item["name"]
#   	price = item["price"]
#   	desc = item["description"]
#   	em.add_field(name = name, value = f'{price} <:coin:791004475098660904> | Описание: {desc}')
#   await ctx.send(embed = em)
#
########################################################################################################


@Bot.event
async def ch_pr():
	await Bot.wait_until_ready()
	pings = [
		"Пошел делать самогон!", "Хочу прибавку к пенсии!",
		"Ушел ебать соседку Риту!", "Заснул старческим сном... Zzzz",
		"Ждет, когда выведут пенсию...", "Пошел пыхнуть на балкон!",
		"Гоняет лысого...", "Пошел на рыбалку!", "Пошел копать огород!",
		"А вот в наше время...........", "Пошел доить корову!",
		"Пошел бухать!", "Отдыхаю на даче!"
		]

	while not Bot.is_closed():
		ping = random.choice(pings)
		await Bot.change_presence(activity=discord.Game(ping))
		await asyncio.sleep(30)



Bot.loop.create_task(ch_pr())
#Bot.run(info["TOKEN"])
Bot.run(info["TOKEN_TEST"])