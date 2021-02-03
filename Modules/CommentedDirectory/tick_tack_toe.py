import json
import asyncio

import discord
from discord.ext import commands as BOT

from Imports.bin import info
from Imports.util import GetMessage


class TickTakToe(BOT.Cog):

	def __init__(self, Bot):
		self.Bot = Bot

	@BOT.command()
	async def stavka(self, ctx, amount):
		with open("JSONs/main.json", "r") as f:
			users = json.load(f)

		bal = [users[str(user.id)]["Wallet"], users[str(user.id)]["Bank"]]

		bal[0] -= amount
		await ctx.send(f"{amount} успешно зарезервированны для игры!")
		rezerv = amount

		with open("Modules/JSONs/reserv.json", "w") as f:
			users = json.load(f)

	@BOT.command()
	async def ttt(self, ctx, member: discord.Member = None):

		player1 = ctx.author.name
		player2 = member.name

		text = player1 + " vs " + player2

		guild = ctx.guild

		if member == ctx.author:
			await ctx.send("Нельзя играть против себя")
			
		elif member == guild.me:
			await ctx.send("Нельзя играть против бота")
			
		else:
			perms = {
				guild.me: discord.PermissionOverwrite(
					read_messages=True,
					send_messages=True),

				ctx.author: discord.PermissionOverwrite(
					read_messages=True,
					send_messages=True),

				member: discord.PermissionOverwrite(
					read_messages=True,
					send_messages=True),

				guild.default_role: discord.PermissionOverwrite(
					read_messages=False)
				}

			channel = await ctx.guild.create_text_channel(
				name=f"{text}",
				overwrites = perms)
		
			await channel.send("__**||@here||**__")
			await channel.send("__**Добро пожаловать в игру: Крестики-Нолики!**__")
			await channel.send("Вы можете поставить ставку на свою победу. Победитель забирает __**ВСЕ!!!**__ . Ожидайте когда бот попросит ввести вашу ставку!")
			
			
			questionList = [
				[f"Игрок {ctx.author} введите свою ставку",
					"Вы можете поставить любое число, даже 0 😈"],

				[f"Игрок {member} введите свою ставку",
					"Вы тоже можете поставить любое число, даже 0 👻 "]
			]

			answers = {}

			for i, question in enumerate(questionList):
				answer = await GetMessage(self.Bot, ctx, question[0], question[1])

				if not answer:
					await ctx.send("Мы не смогли получить ставки или вы их не ввели. Игра звершилась ничьей.")
					return

				answers[i] = answer				

				with open("JSONs/main.json", "r") as f:
					users = json.load(f)
				bal1 = [users[str(ctx.author.id)]["Wallet"],
		users[str(ctx.author.id)]["Bank"]]

				bal2 = [users[str(member.id)]["Wallet"], users[str(member.id)]["Bank"]]

				bal1 -= int(answers[0])
				bal2 -= int(answers[1])

				prize = answers[0] + answers[1]

def setup(Bot):
	Bot.add_cog(TickTakToe(Bot))
