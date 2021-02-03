import discord
from discord.ext import commands as BOT

from Imports.bin import info

pref = info["PREFIX_MAIN"]


class Help(BOT.Cog):

	def __init__(self, Bot):
		self.Bot = Bot

	@BOT.command()
	async def help(self, ctx):
		embed = discord.Embed(
			title="Список команд и их описание",
			description="Зачеркуныте команды временно недоступны ~~{}команда~~".format(pref),
			color=0x7289da)

		embed.add_field(
			name="{}help".format(pref),
			value="Выводит этот список комманд",
			inline=True)

		embed.add_field(
			name="{}cash / balance (_ или (player))".format(pref),
			value="Показывает ваш или баланс другого игрока",
			inline=True)

		embed.add_field(
			name="{}beg / work".format(pref),
			value="Позволяет получить немного денег",
			inline=True)
						
		embed.add_field(
			name="{}deposit (число) / put (число)".format(pref),
			value="Позволяет положить средства в банк для защиты",
			inline=True)

		embed.add_field(
			name="{}withdraw / decision".format(pref),
			value="Команда для снаятия денег в банке",
			inline=True)

		embed.add_field(
			name="{}send (player) (число)".format(pref),
			value="Вы отправить другому игроку деньги",
			inline=True)

		embed.add_field(
			name="{}slots (ставка)".format(pref),
			value="Вы можите сиграть в слоты",
			inline=True)

		embed.add_field(
			name="{}rob (player)".format(pref),
			value="Вы ограбите игрока",
			inline=True)

		embed.add_field(
			name="{}flip (ставка)".format(pref),
			value="Вы подкините монетку, разумеется на деньги",
			inline=True)

		embed.add_field(
			name="{}bonus".format(pref),
			value="Вы узнаете как получить бонус :)",
			inline=True)

		embed.add_field(
			name="{}use (промокод)".format(pref),
			value="Вы получите что-то интересное! ",
			inline=True)
		
		embed.add_field(
			name="{}listpromo".format(pref),
			value="Посмотреть список промокодов, только для админов",
			inline=True)
				
		embed.add_field(
			name="{}del_promo (промокод)".format(pref),
			value="Удалить промокод",
			inline=True)

		embed.add_field(
			name="{}create_promo (промокод) (число активаций)".format(pref),
			value="Создать промокод для с n числои активаций, если n = 0 то безограничений",
			inline=True)
		await ctx.send(embed=embed)


def setup(Bot):
	Bot.add_cog(Help(Bot))
