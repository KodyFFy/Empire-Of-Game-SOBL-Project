import discord
from discord.ext import commands as BOT
from bin import info

pref = info["PREFIX"]

class Help(BOT.Cog):
	
	def __init__(self, Bot):
		self.Bot = Bot

	@BOT.command()
	async def help(self, ctx):
		embed=discord.Embed(title="Список команд и их описание",
							description="Зачеркуныте команды временно недоступны ~~{}команда~~".format(pref),
							color=0x1fefec
							)
		embed.add_field(name="{}help".format(pref), value="Показывает этот список", inline=True)
		embed.add_field(name="{}cash / balance (_ или [player])".format(pref), value="Показывает ваш или баланс игрока", inline=True)
		embed.add_field(name="{}beg / work".format(pref), value="Позволяет получить немного денег", inline=True)
		embed.add_field(name="{}deposit [число] / put [число]".format(pref), value="Позволяет положить средства в банк для защиты", inline=True)
		embed.add_field(name="{}withdraw / decision".format(pref), value="Команда для снаятия денег в банке", inline=True)
		embed.add_field(name="{}send [player] [число]".format(pref), value="Ты отправишь игроку деньги", inline=True)
		embed.add_field(name="{}slots [ставка]".format(pref), value="Ты сыграешь в слоты", inline=True)
		embed.add_field(name="{}rob [player]".format(pref), value="Ты ограбишь игрока", inline=True)


		#embed.add_field(name="~~{}bag~~".format(pref), value="Открыть свой инвентарь", inline=True)
		#embed.add_field(name="~~{}buy~~".format(pref), value="Купить вещь в магазине", inline=True)
		#embed.add_field(name="~~{}sell~~".format(pref), value="Продать купленную вещь", inline=True)
		#embed.add_field(name="~~{}shop~~".format(pref), value="Открыть магазин", inline=True)

		await ctx.send(embed=embed)	


def setup(Bot):
	Bot.add_cog(Help(Bot))