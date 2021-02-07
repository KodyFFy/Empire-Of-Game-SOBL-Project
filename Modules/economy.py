import json
import random
import asyncio

import discord
from discord.ext import commands as BOT

from Imports.bin import info


wait_beg = []
wait_rob = []


class Economy(BOT.Cog):
	def __init__(self, Bot):
		self.Bot = Bot

	@BOT.command(aliases=["cash", "balance"])  # Баланс игрока
	async def __balance(self, ctx, member: discord.Member = None):
		if member is None:
			await open_account(ctx.author)

			user = ctx.author
			users = await get_main_data()

			wallet_amt = int(users[str(user.id)]["Wallet"])
			bank_amt = int(users[str(user.id)]["Bank"])

			await ctx.send(f"Информация о балансе, для игрока {ctx.author.mention}")
			embed = discord.Embed(
				title=f"Баланс пользователя {ctx.author}",
				color=0x7289da)

			embed.add_field(
				name="Баланс",
				value=f"{wallet_amt} <:coin:791004475098660904>")

			embed.add_field(
				name="Банк",
				value=f"{bank_amt} <:coin:791004475098660904>")

			await ctx.send(embed=embed)

		else:
			await open_account(member)

			user = member
			users = await get_main_data()

			wallet_amt = int(users[str(user.id)]["Wallet"])
			bank_amt = int(users[str(user.id)]["Bank"])

			await ctx.send(f"Информация о балансе, игрока {member.mention}")

			embed = discord.Embed(
				title=f"Баланс пользователя {member.name}",
				color=0x7289da)

			embed.add_field(
				name="Баланс ",
				value=f"{wallet_amt} <:coin:791004475098660904>")
			
			embed.add_field(
				name="Банк",
				value=f"{bank_amt} <:coin:791004475098660904>")

			await ctx.send(embed=embed)

	@BOT.command()
	@BOT.has_permissions(administrator=True)
	async def take(self, ctx, member: discord.Member, amount, var="Wallet"):

		await open_account(member)

		users = await get_main_data()
		user = member

		wallet_amt = int(users[str(user.id)]["Wallet"])
		bank_amt = int(users[str(user.id)]["Bank"])

		new_Walletamt = wallet_amt - int(amount)
		new_Bankamt = bank_amt - int(amount)

		if str(var) == "Bank" or str(var) == "bank":
			if new_Bankamt < 0:
				Bank_amt = int(users[str(user.id)]["Bank"])
				await update_bank(member, -1*int(Bank_amt), str(var))

			else:
				await update_bank(member, -1*int(amount), str(var))
				embed = discord.Embed(
					title="Готово!",
					description=f"Админы забрали из банка {amount} <:coin:791004475098660904> у игрока {member.mention}",
					color=0x7289da)
				await ctx.send(embed=embed)

		elif str(var) == "Wallet" or str(var) == "wallet":
			if new_Walletamt < 0:
				Wallet_amt = wallet_amt = int(users[str(user.id)]["Wallet"])
				await update_bank(member, -1*int(Wallet_amt), str(var))

			else:
				await update_bank(member, -1*int(amount), str(var))
			embed = discord.Embed(
				title="Готово!",
				description=f"Админы забрали из кошелька {amount} <:coin:791004475098660904> у игрока {member.mention}",
				color=0x7289da)
			await ctx.send(embed=embed)

		if var is None:
			if new_Walletamt < 0:
				Wallet_amt = wallet_amt = int(users[str(user.id)]["Wallet"])
				await update_bank(member, -1*int(Wallet_amt), str(var))

			else:
				await update_bank(member, -1*int(amount), str(var))
			embed = discord.Embed(
				title="Готово!",
				description=f"Админы забрали из кошелька {amount} <:coin:791004475098660904> у игрока {member.mention}",
				color=0x7289da)
			await ctx.send(embed=embed)

	@BOT.command()
	@BOT.has_permissions(administrator=True)
	async def give(self, ctx, member: discord.Member, amount):
		await open_account(member)
		users = await get_main_data()
		user = ctx.author

		await update_bank(member, 1*int(amount), "Bank")
		embed = discord.Embed(
			title="Готово!",
			description=f"Админы дали игроку {member.mention} {amount} <:coin:791004475098660904>",
			color=0x7289da)
		await ctx.send(embed=embed)

	@BOT.command(aliases=["beg", "work"])  # Работа
	async def __beg(self, ctx):
		await open_account(ctx.author)

		users = await get_main_data()
		user = ctx.author

		earn = random.randrange(300)

		if not str(ctx.author.id) in wait_beg:
			embed = discord.Embed(
				title="Баланс пользователя",
				description=f"Пользователь {ctx.author.mention} получил {earn} <:coin:791004475098660904>!",
				color=0x7289da)
			await ctx.send(embed=embed)

			users[str(user.id)]["Wallet"] += earn
			wait_beg.append(str(ctx.author.id))

			with open("JSONs/main.json", "w") as f:
				json.dump(users, f, indent=4)

			await asyncio.sleep(2*60*60)
			wait_beg.remove(str(ctx.author.id))

		else:
			embed = discord.Embed(
				title="Ошибка!",
				description=f"**{ctx.author.mention}** вы уже использовали эту команду. Команда работает раз в 2 часа.",
				color=0xef3417)
			await ctx.send(embed=embed)

	@BOT.command(aliases=["withdraw", "decision"])  # Снять деньги с банка
	async def __withdraw(self, ctx, amount=None):
		await open_account(ctx.author)
		if amount == None:
			embed = discord.Embed(
				title="Ошибка!",
				description="Введите значение для вывода",
				color=0xef3417)
			await ctx.send(embed=embed)
			return

		bal = await update_bank(ctx.author)
		amount = int(amount)

		if amount > bal[1]:
			embed = discord.Embed(
				title="Ошибка!",
				description="У Вас нет столько <:coin:791004475098660904> на счете **;~;**",
				color=0xef3417)
			await ctx.send(embed=embed)
			return

		if amount < 0:
			embed = discord.Embed(
				title="Ошибка!",
				description="Сумма <:coin:791004475098660904> должна быть положительной!",
				color=0xef3417)
			await ctx.send(embed=embed)
			return

		await update_bank(ctx.author, amount)
		await update_bank(ctx.author, -1*amount, "Bank")
		embed = discord.Embed(title="Готово!", description=f"Вы успешно сняли {amount} <:coin:791004475098660904>",
							  color=0x7289da)
		await ctx.send(embed=embed)

	@BOT.command(aliases=["deposit", "put"])  # Сделать депозит в банке
	async def __deposit(self, ctx, amount=None):
		await open_account(ctx.author)
		if amount == None:
			embed = discord.Embed(
				title="Ошибка!",
				description="Введите значение для вывода <:coin:791004475098660904>",
				color=0xef3417)
			await ctx.send(embed=embed)
			return

		bal = await update_bank(ctx.author)
		amount = int(amount)

		if amount > bal[0]:
			embed = discord.Embed(
				title="Ошибка!",
				description="У Вас нет столько <:coin:791004475098660904> на счете **;~;**",
				color=0xef3417)
			await ctx.send(embed=embed)
			return

		if amount < 0:
			embed = discord.Embed(
				title="Ошибка!",
				description="Сумма <:coin:791004475098660904> должна быть положительной!",
				color=0xef3417)
			await ctx.send(embed=embed)
			return

		await update_bank(ctx.author, -1*amount)
		await update_bank(ctx.author, amount, "Bank")
		embed = discord.Embed(
			title="Готово!",
			description=f"Вы успешно положили на счет {amount} <:coin:791004475098660904>",
			color=0x7289da)
		await ctx.send(embed=embed)

	@BOT.command()  # Отправить деньги
	async def send(self, ctx, member: discord.Member, amount=None):
		await open_account(ctx.author)
		await open_account(member)
		if amount == None:
			embed = discord.Embed(
				title="Ошибка!",
				description="Введите значение для вывода",
				color=0xef3417)
			await ctx.send(embed=embed)
			return

		bal = await update_bank(ctx.author)
		amount = int(amount)

		if amount > bal[1]:
			embed = discord.Embed(
				title="Ошибка!",
				description="У Вас нет столько <:coin:791004475098660904> на счете **;~;**",
				color=0xef3417)
			await ctx.send(embed=embed)
			return

		if amount < 0:
			embed = discord.Embed(
				title="Ошибка!",
				description="Сумма <:coin:791004475098660904> должна быть положительной!",
				color=0xef3417)
			await ctx.send(embed=embed)
			return

		await update_bank(ctx.author, -1*amount, "Bank")
		await update_bank(member, amount, "Bank")
		embed = discord.Embed(
			title="Готово!",
			description=f"Вы успешно перевели пользователю {member.mention} на счет {amount} <:coin:791004475098660904>",
			color=0x7289da)
		await ctx.send(embed=embed)

	@BOT.command()  # Слоты 3*
	async def slots(self, ctx, amount=None):
		await open_account(ctx.author)
		if amount == None:
			embed = discord.Embed(
				title="Ошибка!",
				description="Введите значение ставки!",
				color=0xef3417)
			await ctx.send(embed=embed)
			return

		bal = await update_bank(ctx.author)
		amount = int(amount)
		if amount > bal[0]:
			embed = discord.Embed(
				title="Ошибка!",
				description="У Вас нет столько <:coin:791004475098660904> на счете **;~;**",
				color=0xef3417)
			await ctx.send(embed=embed)
			return

		if amount < 0:
			embed = discord.Embed(
				title="Ошибка!",
				description="Сумма <:coin:791004475098660904> должна быть положительной!",
				color=0xef3417)
			await ctx.send(embed=embed)
			return

		final = []
		for i in range(3):
			a = random.choice(["💰", "💡", "🔋"])
			final.append(a)
		l = " ".join(final)
		await ctx.send("["+str(l)+"]")

		if final[0] == final[1] == final[2]:
			al = amount * 3
			embed = discord.Embed(
				title="**Wow!**",
				description=f"Вы выиграли **ДЖЕКПОТ!** Ты получил {al} <:coin:791004475098660904>",
				color=0x7289da)
			await ctx.send(embed=embed)
			await update_bank(ctx.author, 3*amount)

		else:
			await update_bank(ctx.author, -1*amount)
			embed = discord.Embed(
				title="Вы проиграли!",
				description="Вы проиграли свою ставку! В следующий раз ты точно выиграешь!",
				color=0x7289da)
			await ctx.send(embed=embed)

	@BOT.command()  # Ограбить
	async def rob(self, ctx, member: discord.Member):
		await open_account(ctx.author)
		await open_account(member)

		bal = await update_bank(member)

		if ctx.author.mention == member.mention:
			embed = discord.Embed(
				title="Ошибка!", 
				description="Вы не можете обокрасть самого себя!",
				color=0xef3417)
			await ctx.send(embed=embed)
			return

		if not str(ctx.author.id) in wait_rob:
			if bal[0] < 100:
				embed = discord.Embed(
					title="nope", 
					description="Это действие того не стоит!",
					color=0x7289da)
				await ctx.send(embed=embed)
				return

			earning = int(random.randrange(0, bal[0]//4))
			random_event = random.randint(0, 100)

			if random_event >= 30:
				await update_bank(ctx.author, earning)
				await update_bank(member, -1*earning)
				embed = discord.Embed(
					title="Готово!",
					description=f"Вы удачно обокрали пользователя {member.mention}. Вы своровали {earning} <:coin:791004475098660904>",
					color=0x7289da)
				await ctx.send(embed=embed)

			else:
				plata = int(earning - (earning//4))
				await update_bank(ctx.author, -1*plata)
				await update_bank(member, earning)
				embed = discord.Embed(
					title="Oops...!",
					description=f"Вас поймали за воровство у {member.mention}. Вам выписали штраф в размере {earning} <:coin:791004475098660904>",
					color=0x7289da)
				await ctx.send(embed=embed)

			wait_rob.append(str(ctx.author.id))
			await asyncio.sleep(6*60*60)
			wait_rob.remove(str(ctx.author.id))

		else:
			embed = discord.Embed(
				title="Ошибка!",
				description=f"**{ctx.author.mention}** вы уже использовали эту команду. Команда работает раз в 6 часа.",
				color=0xef3417)
			await ctx.send(embed=embed)


async def open_account(user):
	users = await get_main_data()

	if str(user.id) in users:
		users[str(user.id)]["Name"] = user.name
		with open("JSONs/main.json", "w") as f:
			json.dump(users, f, indent=4)
		return False

	else:
		users[str(user.id)] = {}
		users[str(user.id)]["Name"] = user.name
		users[str(user.id)]["Wallet"] = 0
		users[str(user.id)]["Bank"] = 0

	with open("JSONs/main.json", "w") as f:
		json.dump(users, f, indent=4)
	return True


async def get_main_data():
	with open("JSONs/main.json", "r") as f:
		users = json.load(f)
	return users


async def update_bank(user, change=0, mode="Wallet"):
	users = await get_main_data()
	users[str(user.id)][mode] += change

	with open("JSONs/main.json", "w") as f:
		json.dump(users, f, indent=4)

	bal = [users[str(user.id)]["Wallet"], users[str(user.id)]["Bank"]]
	return bal


def setup(Bot):
	Bot.add_cog(Economy(Bot))

	# @Bot.command() ### Продать предмет
	# async def sell(ctx,item,amount = 1):
	#	await open_account(ctx.author)
	#
	#	res = await sell_this(ctx.author,item,amount)
	#
	#	if not res[0]:
	#		if res[1]==1:
	#			await ctx.send("Такого товара нет!")
	#			return
	#		if res[1]==2:
	#			await ctx.send(f"У тебя не хватает {amount} <:coin:791004475098660904> едениц {item} для продажи.")
	#			return
	#		if res[1]==3:
	#			await ctx.send(f"У тебя нет {item} в рюкзаке.")
	#			return
	#
	#	await ctx.send(f"Ты успешно продал {amount} едениц товара {item}.")
	#
	#
	# @Bot.command() ### Купить предмет
	# async def buy(ctx,item,amount = 1):
	#	await open_account(ctx.author)
	#
	#	res = await buy_this(ctx.author,item,amount)
	#
	#	if not res[0]:
	#		if res[1]==1:
	#			await ctx.send("Такого товара нет!")
	#			return
	#		if res[1]==2:
	#			await ctx.send(f"У тебя не хватате денег чтобы купить {amount} едениц товара {item}")
	#			return
	#
	#
	#	await ctx.send(f"Ты успешно купил {amount} едениц товара {item}")
	#
	# @Bot.command() ### Вывод окна рюкзака
	# async def bag(ctx):
	#	await open_account(ctx.author)
	#	user = ctx.author
	#	users = await get_main_data()
	#
	#	try:
	#		bag = users[str(user.id)]["Bag"]
	#	except:
	#		bag = []
	#
	#
	#	em = discord.Embed(title = "Bag")
	#	for item in bag:
	#		name = item["Item"]
	#		amount = item["Amount"]
	#
	#		em.add_field(name = name, value = amount)
	#
	#	await ctx.send(embed = em)

	# async def buy_this(user,item_name,amount):
	#	item_name = item_name.lower()
	#	name_ = None
	#	for item in mainshop:
	#		name = item["name"].lower()
	#		if name == item_name:
	#			name_ = name
	#			price = item["price"]
	#			break
	#
	#	if name_ == None:
	#		return [False,1]
	#
	#	cost = price*amount
	#
	#	users = await get_main_data()
	#
	#	bal = await update_bank(user)
	#
	#	if bal[0]<cost:
	#		return [False,2]
	#
	#
	#	try:
	#		index = 0
	#		t = None
	#		for thing in users[str(user.id)]["Bag"]:
	#			n = thing["Item"]
	#			if n == item_name:
	#				old_amt = thing["Amount"]
	#				new_amt = old_amt + amount
	#				users[str(user.id)]["Bag"][index]["Amount"] = new_amt
	#				t = 1
	#				break
	#			index+=1
	#		if t == None:
	#			obj = {"Item":item_name , "Amount" : amount}
	#			users[str(user.id)]["Bag"].append(obj)
	#	except:
	#		obj = {"Item":item_name , "Amount" : amount}
	#		users[str(user.id)]["Bag"] = [obj]
	#
	#	with open("JSONs/main.json","w") as f:
	#		json.dump(users, f, indent = 3)
	#
	#	await update_bank(user,cost*-1,"Wallet")
	#
	#	return [True,"Worked"]
	#
	#
	# async def sell_this(user,item_name,amount,price = None):
	#	item_name = item_name.lower()
	#	name_ = None
	#	for item in mainshop:
	#		name = item["name"].lower()
	#		if name == item_name:
	#			name_ = name
	#			if price==None:
	#				price = 0.9* item["price"]
	#			break
	#
	#	if name_ == None:
	#		return [False,1]
	#
	#	cost = price*amount
	#
	#	users = await get_main_data()
	#
	#	bal = await update_bank(user)
	#
	#
	#	try:
	#		index = 0
	#		t = None
	#		for thing in users[str(user.id)]["Bag"]:
	#			n = thing["Item"]
	#			if n == item_name:
	#				old_amt = thing["Amount"]
	#				new_amt = old_amt - amount
	#				if new_amt < 0:
	#					return [False,2]
	#				users[str(user.id)]["Bag"][index]["Amount"] = new_amt
	#				t = 1
	#				break
	#			index+=1
	#		if t == None:
	#			return [False,3]
	#	except:
	#		return [False,3]
	#
	#	with open("JSONs/main.json","w") as f:
	#		json.dump(users, f, indent = 3)
	#
	#	await update_bank(user,cost,"Wallet")
	#
	#	return [True,"Worked"]
	#
