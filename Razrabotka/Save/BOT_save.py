import json
import discord
from discord.ext import commands
import random
from bin import info


Bot = commands.Bot( command_prefix = info['PREFIX'] )

@Bot.event
async def on_ready():
	print("Бот успешно запущен!")

##################################################################################




@Bot.command(aliases = ['cash','balance'])
async def __balance(ctx):

	await open_account(ctx.author)

	user = ctx.author
	users = await get_main_data()

	em = discord.Embed(title = f"Баланс пользователя {ctx.author.name}",color = discord.Color.dark_gold())

	wallet_amt = users[str(user.id)]['Wallet']
	bank_amt = users[str(user.id)]['Bank']

	em.add_field(name = "Баланс", value = wallet_amt)
	em.add_field(name = "Банк", value = bank_amt)

	await ctx.send(embed = em)

@Bot.command(aliases = ['charity','beg'])
async def __beg(ctx):
	await open_account(ctx.author)

	users = await get_main_data()
	user = ctx.author

	earn = random.randrange(100)



	await ctx.send(f"Пользователь {ctx.author} получил {earn} фаеров!")

	users[str(user.id)]['Wallet'] += earn

	with open('main.json','w') as f:
		json.dump(users,f)

async def open_account(user):

	users = await get_main_data()

	if str(user.id) in users:
		return False
	else:
		users[str(user.id)] = {}
		users[str(user.id)]["Wallet"] = 0
		users[str(user.id)]["Bank"] = 0

	with open('main.json','w') as f:
		json.dump(users,f)
	return True


async def get_main_data():
	with open("main.json","r") as f:
		users = json.load(f)

	return users










##################################################################################
Bot.run(info["TOKEN"])