import re
import random
import asyncio

import discord
from discord.ext import commands
from util import GetMessage


time_regex = re.compile(r"(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}


def convert(argument):
    args = argument.lower()
    matches = re.findall(time_regex, args)
    time = 0
    for key, value in matches:
        try:
            time += time_dict[value] * float(key)
        except KeyError:
            raise commands.BadArgument(
                f"{value} is an invalid time key! h|m|s|d are valid arguments"
            )
        except ValueError:
            raise commands.BadArgument(f"{key} не число!")
    return round(time)


class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def giveaway(self, ctx):
        await ctx.send("Давайте создадим форму для Конкурса!")

        questionList = [
            ["В какой канал опубликовать Конкурс?","Какой-то канал."],
            ["Как долго будет идти конкурс?", "`d|h|m|s`"],
            ["Какой приз будет выдна победителю?", "Любой приз"]
        ]

        answers = {}

        for i, question in enumerate(questionList):
            answer = await GetMessage(self.bot, ctx, question[0], question[1])

            if not answer:
                await ctx.send("Ты не успел заполнить форму. Заполняй быстрей!")
                return

            answers[i] = answer
        embed = discord.Embed(name="Конкурс!")
        for key, value in answers.items():
            embed.add_field(name=f"Вопрос: `{questionList[key][0]}`", value=f"Ответ: `{value}`", inline=False)

        m = await ctx.send("Все верно?", embed=embed)
        await m.add_reaction("✅")
        await m.add_reaction("🇽")

        try:
            reaction, member = await self.bot.wait_for(
                "reaction_add",
                timeout=60,
                check=lambda reaction, user: user == ctx.author
                and reaction.message.channel == ctx.channel
            )
        except asyncio.TimeoutError:
            await ctx.send("Ошибка создания. Пожалуйста, попробуйте еще раз.")
            return

        if str(reaction.emoji) not in ["✅", "🇽"] or str(reaction.emoji) == "🇽":
            await ctx.send("Конкурс отменен!")
            return

        channelId = re.findall(r"[0-9]+", answers[0])[0]
        channel = self.bot.get_channel(int(channelId))

        time = convert(answers[1])

        giveawayEmbed = discord.Embed(
            title="🎉 __**Конкурс!**__ 🎉",
            description=answers[2]
        )
        giveawayEmbed.set_footer(text=f"Конкурс окнчится через {time} секунд, после отправки этого сообщения.")
        giveawayMessage = await channel.send(embed=giveawayEmbed)
        await giveawayMessage.add_reaction("🎉")

        await asyncio.sleep(time)

        message = await channel.fetch_message(giveawayMessage.id)
        users = await message.reactions[0].users().flatten()
        users.pop(users.index(ctx.guild.me))
        users.pop(users.index(ctx.author))

        if len(users) == 0:
            await channel.send("Победитель не определен!")
            return

        winner = random.choice(users)

        await channel.send(f"**Поздравляем победителя - {winner.mention}!**\nОбратитесь к {ctx.author.mention} или к админам для получения приза.")


def setup(bot):
    bot.add_cog(Giveaway(bot))