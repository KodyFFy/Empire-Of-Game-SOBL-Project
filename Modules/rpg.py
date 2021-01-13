import discord
from discord.ext import commands as BOT
import json
import random
import asyncio
from bin import info



class RPG(BOT.Cog):
	def __init__(self, Bot):
		self.Bot = Bot


	@BOT.command()
	async def choice(self, ctx, skill):

		with open("Modules/jsons/rpg.json", "r") as f:
			users = json.load(f)
		if str(ctx.author.id) in users:
			await ctx.send("Вы уже выбрали класс")
			return
		elif skill == "DPS":
			users[str(ctx.author.id)] = {}
			users[str(ctx.author.id)]["Class"] = "DPS"
			users[str(ctx.author.id)]["Skills"] = {}
			users[str(ctx.author.id)]["Skills"]["DPS"] = 1
			users[str(ctx.author.id)]["Skills"]["TANK"] = 0
			users[str(ctx.author.id)]["Skills"]["HEALER"] = 0

			with open("Modules/jsons/rpg.json", "w") as f:
				json.dump(users, f, indent = 3)

			await ctx.send("Вы выбрали класс DPS")
		elif skill == "TANK":
			users[str(ctx.author.id)] = {}
			users[str(ctx.author.id)]["Class"] = "TANK"
			users[str(ctx.author.id)]["Skills"] = {}
			users[str(ctx.author.id)]["Skills"]["DPS"] = 0
			users[str(ctx.author.id)]["Skills"]["TANK"] = 1
			users[str(ctx.author.id)]["Skills"]["HEALER"] = 0

			with open("Modules/jsons/rpg.json", "w") as f:
				json.dump(users, f, indent = 2)

			await ctx.send("Вы выбрали класс TANK")
		elif skill == "HEALER":
			users[str(ctx.author.id)] = {}
			users[str(ctx.author.id)]["Class"] = "HEALER"
			users[str(ctx.author.id)]["Skills"] = {}
			users[str(ctx.author.id)]["Skills"]["DPS"] = 0
			users[str(ctx.author.id)]["Skills"]["TANK"] = 0
			users[str(ctx.author.id)]["Skills"]["HEALER"] = 1

			with open("Modules/jsons/rpg.json", "w") as f:
				json.dump(users, f, indent = 2)

			await ctx.send("Вы выбрали класс HEALER")

	@BOT.command()
	async def rechoice(self, ctx, skill):

		with open("Modules/jsons/rpg.json", "r") as f:
			users = json.load(f)

		if skill == "DPS":
			users[str(ctx.author.id)] = {}
			users[str(ctx.author.id)]["Class"] = "DPS"
			users[str(ctx.author.id)]["Skills"] = {}
			users[str(ctx.author.id)]["Skills"]["DPS"] = 1
			users[str(ctx.author.id)]["Skills"]["TANK"] = 0
			users[str(ctx.author.id)]["Skills"]["HEALER"] = 0

			with open("Modules/jsons/rpg.json", "w") as f:
				json.dump(users, f, indent = 2)

			await ctx.send("Вы выбрали класс DPS")
		elif skill == "TANK":
			users[str(ctx.author.id)] = {}
			users[str(ctx.author.id)]["Class"] = "TANK"
			users[str(ctx.author.id)]["Skills"] = {}
			users[str(ctx.author.id)]["Skills"]["DPS"] = 0
			users[str(ctx.author.id)]["Skills"]["TANK"] = 1
			users[str(ctx.author.id)]["Skills"]["HEALER"] = 0

			with open("Modules/jsons/rpg.json", "w") as f:
				json.dump(users, f, indent = 2)

			await ctx.send("Вы выбрали класс TANK")
		elif skill == "HEALER":
			users[str(ctx.author.id)] = {}
			users[str(ctx.author.id)]["Class"] = "HEALER"
			users[str(ctx.author.id)]["Skills"] = {}
			users[str(ctx.author.id)]["Skills"]["DPS"] = 0
			users[str(ctx.author.id)]["Skills"]["TANK"] = 0
			users[str(ctx.author.id)]["Skills"]["HEALER"] = 1

			with open("Modules/jsons/rpg.json", "w") as f:
				json.dump(users, f, indent = 2)

			await ctx.send("Вы выбрали класс HEALER")

	@BOT.command()
	async def train(self, ctx, skill):

		with open("Modules/jsons/rpg.json", "r") as f:
			users = json.load(f)
		lvlup = random.uniform(0.05,0.35)
		print(lvlup)
		lvlup = round(lvlup,3)
		print(lvlup)
		lvl_skill =  users[str(ctx.author.id)]["Skills"][str(skill)]
		clas = users[str(ctx.author.id)]["Class"]






		if clas == "DPS":
			maxDPSlvl = 10
			maxTANKlvl = 3
			maxHEALERlvl = 4

			if skill == "DPS" and lvl_skill > maxDPSlvl:
				users[str(ctx.author.id)]["Skills"][str(skill)] = maxDPSlvl
				await ctx.send(f"Уровень скила {skill} максимален")
			elif skill == "DPS"  and lvl_skill < maxDPSlvl:
				users[str(ctx.author.id)]["Skills"][str(skill)] += lvlup
				await ctx.send(f"Ваш уровень скила {skill} повышен на {lvlup}")

			if skill == "TANK" and lvl_skill > maxTANKlvl:
				users[str(ctx.author.id)]["Skills"][str(skill)] = maxTANKlvl
				await ctx.send(f"Уровень скила {skill} максимален")
			elif skill == "TANK" and lvl_skill < maxTANKlvl:
				users[str(ctx.author.id)]["Skills"][str(skill)] += lvlup
				await ctx.send(f"Ваш уровень скила {skill} повышен на {lvlup}")

			if skill == "HEALER" and lvl_skill > maxHEALERlvl:
				users[str(ctx.author.id)]["Skills"][str(skill)] = maxHEALERlvl
				await ctx.send(f"Уровень скила {skill} максимален")
			elif skill == "HEALER" and lvl_skill < maxHEALERlvl:
				users[str(ctx.author.id)]["Skills"][str(skill)] += lvlup
				await ctx.send(f"Ваш уровень скила {skill} повышен на {lvlup}")

		with open("Modules/jsons/rpg.json", "w") as f:
			json.dump(users, f, indent = 2)

		if clas == "TANK":

			maxDPSlvl = 3
			maxTANKlvl = 10
			maxHEALERlvl = 2

			if skill == "DPS" and lvl_skill > maxDPSlvl:
				users[str(ctx.author.id)]["Skills"][str(skill)] = maxDPSlvl
				await ctx.send(f"Уровень скила {skill} максимален")
			elif skill == "DPS"  and lvl_skill < maxDPSlvl:
				users[str(ctx.author.id)]["Skills"][str(skill)] += lvlup
				await ctx.send(f"Ваш уровень скила {skill} повышен на {lvlup}")

			if skill == "TANK" and lvl_skill > maxTANKlvl:
				users[str(ctx.author.id)]["Skills"][str(skill)] = maxTANKlvl
				await ctx.send(f"Уровень скила {skill} максимален")
			elif skill == "TANK" and lvl_skill < maxTANKlvl:
				users[str(ctx.author.id)]["Skills"][str(skill)] += lvlup
				await ctx.send(f"Ваш уровень скила {skill} повышен на {lvlup}")

			if skill == "HEALER" and lvl_skill > maxHEALERlvl:
				users[str(ctx.author.id)]["Skills"][str(skill)] = maxHEALERlvl
				await ctx.send(f"Уровень скила {skill} максимален")
			elif skill == "HEALER" and lvl_skill < maxHEALERlvl:
				users[str(ctx.author.id)]["Skills"][str(skill)] += lvlup
				await ctx.send(f"Ваш уровень скила {skill} повышен на {lvlup}")

		if clas == "HEALER":

			maxDPSlvl = 4
			maxTANKlvl = 1
			maxHEALERlvl = 10

			if skill == "DPS" and lvl_skill > maxDPSlvl:
				users[str(ctx.author.id)]["Skills"][str(skill)] = maxDPSlvl
				await ctx.send(f"Уровень скила {skill} максимален")
			elif skill == "DPS"  and lvl_skill < maxDPSlvl:
				users[str(ctx.author.id)]["Skills"][str(skill)] += lvlup
				await ctx.send(f"Ваш уровень скила {skill} повышен на {lvlup}")

			if skill == "TANK" and lvl_skill > maxTANKlvl:
				users[str(ctx.author.id)]["Skills"][str(skill)] = maxTANKlvl
				await ctx.send(f"Уровень скила {skill} максимален")
			elif skill == "TANK" and lvl_skill < maxTANKlvl:
				users[str(ctx.author.id)]["Skills"][str(skill)] += lvlup
				await ctx.send(f"Ваш уровень скила {skill} повышен на {lvlup}")

			if skill == "HEALER" and lvl_skill > maxHEALERlvl:
				users[str(ctx.author.id)]["Skills"][str(skill)] = maxHEALERlvl
				await ctx.send(f"Уровень скила {skill} максимален")
			elif skill == "HEALER" and lvl_skill < maxHEALERlvl:
				users[str(ctx.author.id)]["Skills"][str(skill)] += lvlup
				await ctx.send(f"Ваш уровень скила {skill} повышен на {lvlup}")


	@BOT.command()
	async def lvl():



		embed=discord.Embed(title="**Статистика ваших классов**", description="Выбранный класс: КЛАСС ", color=0x212ee4)
		embed.add_field(name="DPS", value="уровень; Макс. Уровень", inline=False)
		embed.add_field(name="TANK", value="уровень; Макс. Уровень", inline=False)
		embed.add_field(name="HEALER", value="уровень; Макс. Уровень", inline=False)
		await ctx.send(embed=embed)			
def setup(Bot):
	Bot.add_cog(RPG(Bot))