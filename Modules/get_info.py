import requests as req
from bs4 import BeautifulSoup
 
import discord
from discord.ext import commands as BOT

class Get_Info(BOT.Cog):
	def __init__(self, Bot):
		self.Bot = Bot

	@BOT.command()
	async def epicgames(self, ctx):
		r = req.get("https://www.epicgames.com/store/ru/").text

		soup = BeautifulSoup(r, "lxml")

		block = soup.find("div", {"class": "css-1x2owq5-DiscoverContainerHighlighted__root"})
		
		#game_block = block.find("section", {"class": "css-1nzrk0w-CardGrid-styles__groupWrapper"})


		#game = block.find("span", {"data-testid": "offer-title-info-title", "class":"css-2ucwu", "data-component":"OfferTitleInfo"})

		#game_name = game_block.find("span", {"data-testid": "offer-title-info-title", "class": "css-2ucwu", "data-component": "OfferTitleInfo"})

		#print(game_name.text)
		print(block)

def setup(Bot):
	Bot.add_cog(Get_Info(Bot))
