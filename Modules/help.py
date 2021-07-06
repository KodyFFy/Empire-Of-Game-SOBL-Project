import discord
from discord.ext import commands as BOT

from bot import ArgParser

class Help(BOT.Cog):
    def __init__(self, Bot):
        self.Bot = Bot

    @BOT.command()
    async def help(self, ctx):
        embed = discord.Embed(
            title="Список команд и их описание",
            description="Зачеркуныте команды временно недоступны "
                       f"~~{ArgParser.pref}команда~~",
            color=0x7289da)

        embed.add_field(
            name=f"{ArgParser.pref}help",
            value="Выводит этот список комманд",
            inline=True)

        embed.add_field(
            name=f"{ArgParser.pref}cash / balance (или @player)",
            value="Показывает ваш или баланс другого игрока",
            inline=True)

        embed.add_field(
            name=f"{ArgParser.pref}beg / work",
            value="Позволяет получить немного денег",
            inline=True)

        embed.add_field(
            name=f"{ArgParser.pref}deposit (число) / put (число)",
            value="Позволяет положить средства в банк для защиты",
            inline=True)

        embed.add_field(
            name=f"{ArgParser.pref}withdraw / decision",
            value="Команда для снаятия денег в банке",
            inline=True)

        embed.add_field(
            name=f"{ArgParser.pref}send (player) (число)",
            value="Вы отправить другому игроку деньги",
            inline=True)

        embed.add_field(
            name=f"{ArgParser.pref}slots (ставка)",
            value="Вы можите сиграть в слоты",
            inline=True)

        embed.add_field(
            name=f"{ArgParser.pref}rob (player)",
            value="Вы ограбите игрока",
            inline=True)

        embed.add_field(
            name=f"{ArgParser.pref}flip (ставка)",
            value="Вы подкините монетку, разумеется на деньги",
            inline=True)

        embed.add_field(
            name=f"{ArgParser.pref}bonus",
            value="Вы узнаете как получить бонус :)",
            inline=True)

        embed.add_field(
            name=f"{ArgParser.pref}use (промокод)",
            value="Вы получите что-то интересное! ",
            inline=True)

        embed.add_field(
            name=f"{ArgParser.pref}listpromo",
            value="Посмотреть список промокодов, только для админов",
            inline=True)

        embed.add_field(
            name=f"{ArgParser.pref}del_promo (промокод)",
            value="Удалить промокод",
            inline=True)

        embed.add_field(
            name=f"{ArgParser.pref}create_promo (промокод) (число активаций)",
            value="Создать промокод для с n числои активаций, "
                  "если n=0, то безограничений",
            inline=True)

"""
        embed.add_field(
            name=f"{ArgParser.pref}e?expression (число)",
            value="Математическая игра",
            inline=Thue
        )
        await ctx.send(embed=embed)
"""


def setup(Bot):
    Bot.add_cog(Help(Bot))
