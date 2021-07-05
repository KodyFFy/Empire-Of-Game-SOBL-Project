import json
import random
import asyncio
import requests
from bs4 import BeautifulSoup

import discord
from discord.ext import commands as BOT

from config import info
import Modules.economy as econom


class Reactions(BOT.Cog):
	def __init__(self, Bot):
		self.Bot = Bot
	
	@BOT.command()     ### Сказать, что выебешь в жопу ツ
	async def fuckyou(self, ctx, member: discord.Member):
		num = random.randint(1, 15)
		name = str(num) + ".gif"

		await ctx.send(f"{ctx.author.mention} послал на хуй {member.mention}")
		await ctx.send(file=discord.File(f"./Images/GIFS/Fuck_You/{name}"))
	
	@BOT.command()     ### Сказать Доброе Утро!
	async def hey(self, ctx, member: discord.Member = None):
		num = random.randint(1, 11)
		name = str(num) + ".gif"

		mass_all = ["поприветствовал всех!", "поздоровался со всеми!", "сказал Салам Алейкум всем!","сказал всем ДОБРОЕ УТРО!", "сказал всем дратути!", "сказал всем КУ", "сказал всем салют!", "сказал всем ЙО!"]
		mass_target = ["поприветствовал ", "поздоровался с ", "сказал Салам Алейкум ","сказал ДОБРОЕ УТРО ", "сказал КУ ", "сказал салют ", "сказал ЙО "]

		r_all = random.choice(mass_all)
		r_target = random.choice(mass_target)

		if member == None:
			await ctx.send(f"{ctx.author.mention} {r_all}")
			await ctx.send(file=discord.File(f"./Images/GIFS/Hey/{name}"))
		await ctx.send(f"{ctx.author.mention} {r_target} {member.mention}")
		await ctx.send(file=discord.File(f"./Images/GIFS/Hey/{name}"))

	@BOT.command()    ### Сказать прощай
	async def bye(self, ctx, member: discord.Member):
		num = random.randint(1, 5)
		name = str(num) + ".gif"

		await ctx.send(f"{ctx.author.mention} сказа пока {member.mention}")
		await ctx.send(file=discord.File(f"./Images/GIFS/Bye/{name}"))

	@BOT.command()    ### Дать кому-то по ебалу :) (действительно)
	async def hit(self, ctx, member: discord.Member):
		num = random.randint(1, 15)
		name = str(num) + ".gif"

		await ctx.send(f"{ctx.author.mention} дает люлей {member.mention}!!!")
		await ctx.send(file=discord.File(f"./Images/GIFS/Hit/{name}"))
 
	@BOT.command()     ### Позвать кого-то поиграть 
	async def letsplay(self, ctx, member: discord.Member, game=None):
		num = random.randint(1, 3)
		name = str(num) + ".gif"
		if game == None:
			await ctx.send(f"{ctx.author.mention} зовет играть {member.mention}")
			await ctx.send(file=discord.File(f"./Images/GIFS/Play/{name}"))
		else:
			await ctx.send(f"{ctx.author.mention} зовет играть {member.mention} в **{game}**")
			await ctx.send(file=discord.File(f"./Images/GIFS/Play/{name}"))

def setup(Bot):
	Bot.add_cog(Reactions(Bot))
