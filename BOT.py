import json
import discord
from discord.ext import commands
import random
from bin import info
import asyncio
import datetime

pref = info['PREFIX']
Bot = commands.Bot( command_prefix = pref )
name_Shop_id = "Roles"

wait_beg = []
wait_rob = []


@Bot.event
async def on_ready():
	print("Бот успешно запущен!")
### Розыгрыши ###




##################################################################################

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

Bot.remove_command('help')
@Bot.command()
async def help(ctx):



	embed=discord.Embed(title="Список команд и их описание", description="Зачеркуныте команды временно недоступны ~~{}команда~~".format(pref), color=0x1fefec)
	embed.add_field(name="{}help".format(pref), value="Показывает этот список", inline=True)
	embed.add_field(name="{}cash / balance (_ или [player])".format(pref), value="Показывает ваш или баланс игрока", inline=True)
	embed.add_field(name="{}beg / work".format(pref), value="Позволяет получить немного денег", inline=True)
	embed.add_field(name="{}deposit [число] / put [число]".format(pref), value="Позволяет положить средства в банк для защиты", inline=True)
	embed.add_field(name="{}withdraw / decision".format(pref), value="Команда для снаятия денег в банке", inline=True)
	embed.add_field(name="{}send [player] [число]".format(pref), value="Ты отправишь игроку деньги", inline=True)
	embed.add_field(name="{}slots [ставка]".format(pref), value="Ты сыграешь в слоты", inline=True)
	embed.add_field(name="{}rob [player]".format(pref), value="Ты ограбишь игрока", inline=True)


	embed.add_field(name="~~{}bag~~".format(pref), value="Открыть свой инвентарь", inline=True)
	embed.add_field(name="~~{}buy~~".format(pref), value="Купить вещь в магазине", inline=True)
	embed.add_field(name="~~{}sell~~".format(pref), value="Продать купленную вещь", inline=True)
	embed.add_field(name="~~{}shop~~".format(pref), value="Открыть магазин", inline=True)

	await ctx.send(embed=embed)



@Bot.command() ### Продать предмет
async def sell(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await sell_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("Такого товара нет!")
            return
        if res[1]==2:
            await ctx.send(f"У тебя не хватает {amount} <:coin:791004475098660904> едениц {item} для продажи.")
            return
        if res[1]==3:
            await ctx.send(f"У тебя нет {item} в рюкзаке.")
            return

    await ctx.send(f"Ты успешно продал {amount} едениц товара {item}.")


@Bot.command() ### Купить предмет
async def buy(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await buy_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("Такого товара нет!")
            return
        if res[1]==2:
            await ctx.send(f"У тебя не хватате денег чтобы купить {amount} едениц товара {item}")
            return


    await ctx.send(f"Ты успешно купил {amount} едениц товара {item}")


@Bot.command() ### Вывод окна рюкзака
async def bag(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_main_data()

    try:
        bag = users[str(user.id)]["Bag"]
    except:
        bag = []


    em = discord.Embed(title = "Bag")
    for item in bag:
        name = item["Item"]
        amount = item["Amount"]

        em.add_field(name = name, value = amount)    

    await ctx.send(embed = em) 



@Bot.command(aliases = ['cash','balance']) ### Баланс карточка
async def __balance(ctx, member: discord.Member = None):



	
	if member is None:

		await open_account(ctx.author)

		user = ctx.author
		
		users = await get_main_data()
		
		await ctx.send(f"Информация о балансе, для игрока {ctx.author.mention}")
                

                
		
		emb = discord.Embed(title = f"Баланс пользователя {ctx.author}",color = discord.Color.dark_gold())

		wallet_amt = users[str(user.id)]['Wallet']
		bank_amt = users[str(user.id)]['Bank']

		emb.add_field(name = "Баланс ", value = f"{wallet_amt} <:coin:791004475098660904>")
		emb.add_field(name = "Банк", value = f"{bank_amt} <:coin:791004475098660904>")

		await ctx.send(embed = emb)
	else: 
		await open_account(member)
		user = member
		users = await get_main_data()
		await ctx.send(f"Информация о балансе, игрока {member.mention}")
		em = discord.Embed(title = f"Баланс пользователя {member.name}",color = discord.Color.dark_gold())

		wallet_amt = users[str(user.id)]['Wallet']
		bank_amt = users[str(user.id)]['Bank']

		em.add_field(name = "Баланс ", value = f"{wallet_amt} <:coin:791004475098660904>")
		em.add_field(name = "Банк", value = f"{bank_amt} <:coin:791004475098660904>")

		await ctx.send(embed = em)


@Bot.command()
@commands.has_permissions(administrator= True)
async def take(ctx, member: discord.Member , amount , var = "Wallet"):

	await open_account(member)

	users = await get_main_data()
	user = member


	wallet_amt = users[str(user.id)]['Wallet']
	bank_amt = users[str(user.id)]['Bank']	

	new_Walletamt = wallet_amt - int(amount)
	new_Bankamt = bank_amt - int(amount)




	if str(var) == "Bank" or str(var) == "bank":
				if new_Bankamt < 0:
					Bank_amt = users[str(user.id)]['Bank']
					await update_bank(member, -1*int(Bank_amt),str(var))
				else:	
					await update_bank(member, -1*int(amount),str(var))
				await ctx.send(f"Админы забрали из банка {amount} <:coin:791004475098660904> у игрока {member.mention}")
	elif str(var) == "Wallet"  or str(var) == "wallet":

				if new_Walletamt < 0:
					Wallet_amt = wallet_amt = users[str(user.id)]['Wallet']
					await update_bank(member, -1*int(Wallet_amt),str(var))
				else:
					await update_bank(member, -1*int(amount),str(var))
				await ctx.send(f"Админы забрали из кошелька {amount} <:coin:791004475098660904> у игрока {member.mention}")
	if var is None:
				if new_Walletamt < 0:
					Wallet_amt = wallet_amt = users[str(user.id)]['Wallet']
					await update_bank(member, -1*int(Wallet_amt),str(var))
				else:
					await update_bank(member, -1*int(amount),str(var))
				await ctx.send(f"Админы забрали из кошелька {amount} <:coin:791004475098660904> у игрока {member.mention}")
					
@Bot.command()
@commands.has_permissions(administrator= True)
async def give(ctx, member: discord.Member , amount):

	await open_account(member)

	users = await get_main_data()
	user = ctx.author

	await update_bank(member, 1*int(amount),"Bank")
	await ctx.send(f"Админы дали игроку {member.mention} {amount} <:coin:791004475098660904>")

@Bot.command(aliases = ['beg','work']) ### Работать
async def __beg(ctx):
	await open_account(ctx.author)

	users = await get_main_data()
	user = ctx.author

	earn = random.randrange(300)





	if not str(ctx.author.id) in wait_beg:


		
		await ctx.send(f"Пользователь {ctx.author.mention} получил {earn} <:coin:791004475098660904>!")


		users[str(user.id)]['Wallet'] += earn

		wait_beg.append(str(ctx.author.id))


		with open('main.json','w') as f:
			json.dump(users,f)


		await asyncio.sleep(2*60*60)

		wait_beg.remove(str(ctx.author.id))


	else:
		emb = discord.Embed(description = f'**{ctx.author.mention}** вы уже использовали эту команду. Команда работает раз в 2 часа.')		
		await ctx.send(embed = emb)



@Bot.command(aliases = ['withdraw','decision']) ### Снять деньги с банка
async def __withdraw(ctx, amount = None):
	await open_account(ctx.author)
	if amount == None:
		await ctx.send("Введите значение для вывода")
		return
	bal = await update_bank(ctx.author)

	amount = int(amount)

	if amount > bal[1]:
		await ctx.send("У тебя нет столько <:coin:791004475098660904> на счете :(")
		return
	if amount<0:
		await ctx.send("Сумма <:coin:791004475098660904> должна быть положительной")
		return

	await update_bank(ctx.author, amount)
	await update_bank(ctx.author, -1*amount, "Bank")
	await ctx.send(f"Ты успешно снял {amount} <:coin:791004475098660904>")



@Bot.command(aliases = ['deposit','put']) ### Сделать депозит в банке
async def __deposit(ctx, amount = None):
	await open_account(ctx.author)
	if amount == None:
		await ctx.send("Введите значение для вывода <:coin:791004475098660904>")
		return
	bal = await update_bank(ctx.author)

	amount = int(amount)

	if amount > bal[0]:
		await ctx.send("У тебя нет столько <:coin:791004475098660904> на счете :(")
		return
	if amount<0:
		await ctx.send("Сумма должна быть положительной")
		return

	await update_bank(ctx.author, -1*amount)
	await update_bank(ctx.author, amount, "Bank")
	await ctx.send(f"Ты успешно положил на счет {amount} <:coin:791004475098660904>")



@Bot.command() ### Отправить деньги
async def send(ctx, member: discord.Member,amount = None):
	await open_account(ctx.author)
	await open_account(member)
	if amount == None:
		await ctx.send("Введите значение для вывода")
		return
	bal = await update_bank(ctx.author)

	amount = int(amount)

	if amount > bal[1]:
		await ctx.send("У тебя нет столько <:coin:791004475098660904> на счете :(")
		return
	if amount<0:
		await ctx.send("Сумма должна быть положительной")
		return

	await update_bank(ctx.author, -1*amount, "Bank")
	await update_bank(member, amount, "Bank")
	await ctx.send(f"Ты успешно перевел пользователю {member.mention} на счет {amount} <:coin:791004475098660904>")


@Bot.command() ### Слоты 3*
async def slots(ctx,amount = None):

	await open_account(ctx.author)
	if amount == None:
		await ctx.send("Введите значение для вывода")
		return
	bal = await update_bank(ctx.author)

	amount = int(amount)

	if amount > bal[0]:
		await ctx.send("У тебя нет столько <:coin:791004475098660904> на счете :(")
		return
	if amount<0:
		await ctx.send("Сумма должна быть положительной")
		return

	final = []
	for i in range(3):
		a = random.choice(["💰","💡","🔋"])
		final.append (a)
	l = ' '.join(final)
	await ctx.send("["+str(l)+"]")

	if final[0] == final[1] == final[2]:
		al = amount * 3
		await ctx.send(f"Ты выиграл ДЖЕКПОТ! Ты получил {al} <:coin:791004475098660904>")
		await update_bank(ctx.author, 3*amount)


	elif final[0] == final[1]  or final[1] == final[2]:
		await update_bank(ctx.author, 1.5*amount)
		al = amount * 1.5
		await ctx.send(f"Ты выиграл! Ты получил {al} <:coin:791004475098660904>")

	else: 
		await update_bank(ctx.author, -1*amount)
		await ctx.send("Ты проиграл свою ставку!")

@Bot.command() ### Ограбить
async def rob(ctx, member: discord.Member):
	await open_account(ctx.author)
	await open_account(member)

	bal = await update_bank(member)






	if not str(ctx.author.id) in wait_rob:

		if bal[0]<100:
			await ctx.send("Это действие того не стоит!")
			return

		earning = random.randrange(0,bal[0]//3)


		random_event = random.randint(0,100)

		if random_event >= 30:
			await update_bank(ctx.author, earning)
			await update_bank(member, -1*earning)
			await ctx.send(f"Ты удачно обокрал пользователя {member.mention}. Ты своровал {earning} <:coin:791004475098660904>")
		else:
			plata = earning - (earning/3)
			await update_bank(ctx.author, -1*palata)
			await update_bank(member, earning)
			await ctx.send(f"Тебя поймали за воровство у {member.mention}. Тебе выписали штраф {earning} <:coin:791004475098660904>")

		wait_rob.append(str(ctx.author.id))

		await asyncio.sleep(6*60*60)

		wait_rob.remove(str(ctx.author.id))

	else:


		emb = discord.Embed(description = f'**{ctx.author.mention}** вы уже использовали эту команду. Команда работает раз в 6 часов.')		
		await ctx.send(embed = emb)




################### Функции для экономики ###################


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

async def update_bank(user, change = 0, mode = "Wallet"):
	users = await get_main_data()

	users[str(user.id)][mode] += change

	with open('main.json','w') as f:
		json.dump(users,f)
	bal = [users[str(user.id)]["Wallet"],users[str(user.id)]["Bank"]]
	return  bal



async def buy_this(user,item_name,amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_main_data()

    bal = await update_bank(user)

    if bal[0]<cost:
        return [False,2]


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["Bag"]:
            n = thing["Item"]
            if n == item_name:
                old_amt = thing["Amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["Bag"][index]["Amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            obj = {"Item":item_name , "Amount" : amount}
            users[str(user.id)]["Bag"].append(obj)
    except:
        obj = {"Item":item_name , "Amount" : amount}
        users[str(user.id)]["Bag"] = [obj]        

    with open("main.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost*-1,"Wallet")

    return [True,"Worked"]


async def sell_this(user,item_name,amount,price = None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price==None:
                price = 0.9* item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_main_data()

    bal = await update_bank(user)


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["Bag"]:
            n = thing["Item"]
            if n == item_name:
                old_amt = thing["Amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False,2]
                users[str(user.id)]["Bag"][index]["Amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            return [False,3]
    except:
        return [False,3]    

    with open("main.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost,"Wallet")

    return [True,"Worked"]

################### Функции для экономики ###################



##################################################################################

@Bot.event
async def ch_pr():
	await Bot.wait_until_ready()

	pings = ["Пошел делать самогон!","Хочу прибавку к пенсии!","Ушел ебать соседку Риту!","Заснул старческим сном... Zzzz"]

	while not Bot.is_closed():

		ping = random.choice(pings)
		await Bot.change_presence(activity=discord.Game(ping))

		await asyncio.sleep(10)

Bot.loop.create_task(ch_pr())
Bot.run(info["TOKEN"])
