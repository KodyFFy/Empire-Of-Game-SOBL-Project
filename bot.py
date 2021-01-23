import json
import discord
from discord.ext import commands
import random
from Imports.bin import info
import asyncio
import logging
import os



os.remove("Logs/discord_befor.log")


os.rename("Logs/discord_correct.log","Logs/discord_befor.log")

logging.basicConfig(level=logging.INFO)


file_new = open("Logs/discord_correct.log",'w+')
file_new.close()


logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='Logs/discord_correct.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(name)s: %(message)s'))
logger.addHandler(handler)

# pref = info['PREFIX_MAIN']
pref = info["PREFIX_TEST"]

Bot = commands.Bot(command_prefix=pref)
name_Shop_id = "Roles"


@Bot.event
async def on_ready():
	print(f"Бот успешно запущен!")
Bot.remove_command('help')


@Bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		embed=discord.Embed(title="Ошибка!",
			description=f"Неверный аргумент, попробуйте `{pref}help` что-бы узнать больше о командах.",
			color=0xef3417)
		await ctx.send(embed=embed)

	if isinstance(error, commands.CommandNotFound):
		embed=discord.Embed(title="Ошибка!",
			description=f"Такой команды не существует! Попробуйте воспользутесь командой `{pref}help`!",
			color=0xef3417)
		await ctx.send(embed=embed)

Bot.load_extension("Modules.help")
Bot.load_extension("Modules.economy")
Bot.load_extension("Modules.giveaway")
Bot.load_extension("Modules.flip_coin")
Bot.load_extension("Modules.bones")

#Bot.load_extension("Modules.tick_tack_toe")

# Bot.load_extension("Modules.rpg")

########################################################################################################
#
# mainshop = [{"name":"Watch","price":100,"description":"Time"},
#            {"name":"Laptop","price":1000,"description":"Work"},
#            {"name":"PC","price":10000,"description":"Gaming"}]
#
#
# @Bot.command() ### Вывыод окна магазина 
# async def shop(ctx):
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
async def __change_pings():
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


Bot.loop.create_task(__change_pings())

#Bot.run(info["TOKEN_MAIN"])
Bot.run(info["TOKEN_TEST"])
