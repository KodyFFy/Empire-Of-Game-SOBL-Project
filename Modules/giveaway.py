import re
import random
import asyncio
import json

import discord
from discord.ext import commands

from Imports.util import GetMessage
import Modules.economy as economy


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
                f"{value} is an invalid time key! "
                 "h|m|s|d are valid arguments")

        except ValueError:
            raise commands.BadArgument(f"{key} не число!")
    return round(time)


class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role("Призовщик")
    async def giveaway(self, ctx):
        await ctx.send("Давайте создадим форму для Конкурса!")

        questionList = [
            ["В какой канал опубликовать Конкурс?", "Какой-то канал."],
            ["Как долго будет идти конкурс?", "`d|h|m|s`"],
            ["Какой приз будет выдан победителю?", "Любой приз"]
        ]

        answers = {}

        for i, question in enumerate(questionList):
            answer = await GetMessage(self.bot, ctx, question[0], question[1])

            if not answer:
                embed=discord.Embed(title="Ошибка!",
                    description="Вы не устели заполнить форму? "
                                "Значит заполняйте быстрее...",
                    color=0xef3417)
                await ctx.send(embed=embed)
                return

            answers[i] = answer
        embed = discord.Embed(name="Конкурс!")

        for key, value in answers.items():
            embed.add_field(
                name=f"Вопрос: `{questionList[key][0]}`",
                value=f"Ответ: `{value}`",
                inline=False)

        m = await ctx.send("Все верно?", embed=embed)
        await m.add_reaction("✅")
        await m.add_reaction("🇽")

        try:
            reaction, member = await self.bot.wait_for(
                "reaction_add",
                timeout=60,
                check=lambda reaction, user: user == ctx.author
                and reaction.message.channel == ctx.channel)

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
            description=answers[2])

        giveawayEmbed.set_footer(
            text=f"Конкурс окнчится через {time} секунд, "
                  "после отправки этого сообщения.")

        await channel.send("||@here|| Начало Конкурса!")

        giveawayMessage = await channel.send(embed=giveawayEmbed)
        await giveawayMessage.add_reaction("🎉")

        await asyncio.sleep(time)

        message = await channel.fetch_message(giveawayMessage.id)
        users = await message.reactions[0].users().flatten()
        users.pop(users.index(ctx.guild.me))

        if ctx.author in users:
            users.pop(users.index(ctx.author))

        if len(users) == 0:
            await channel.send("Победитель не определен!")
            return

        winner = random.choice(users)
        spl = answers[2].split()

        if spl[1] == "<:coin:791004475098660904>" or spl[1] == "\U0001fa99":
            user = winner
            await economy.open_account(user)

            users = await economy.get_main_data()
            users[str(user.id)]["Bank"] += int(spl[0])

            with open("JSONs/main.json", "w") as f:
                json.dump(users, f, indent = 3)

            await channel.send("**Поздравляем победителя - "
                               f"{winner.mention}!**\nВам зачисленно на счет "
                               f"{answers[2]}.")

        else:
            await channel.send("**Поздравляем победителя - "
                              f"{winner.mention}!**\nОбратитесь к "
                              f"{ctx.author.mention} или к админам "
                              f"для получения приза {answers[2]}.")

"""
    @commands.command(aliases=["Raid", "raid"])
    @commands.has_permissions(administrator=True)
    async def __raid(self, ctx):

    	questionList = [
    		["В какой канал опубликовать ивент?", "Какой-то канал."],
    		["Как долго будет идти ивент?", "`d|h|m|s`"],
    		["Сложность", "Любая сложность(Легко, Сложно)"],
    		["Какой лучший приз будет получен?", "Любой лучший приз"],
    		["Какой обычный приз будет получен?", "Любой приз"],
    		["Какой штраф будет при пройгрыше", "Например: Понижение"]
    	]

    	answers = {}

    	for i, question in enumerate(questionList):
    		answer = await GetMessage(self.bot, ctx, question[0], question[1])

    		if not answer:
    			await ctx.send(
                  "Ты не успел заполнить форму. Заполняй быстрей!")
    			return

    		answers[i] = answer
    	embed = discord.Embed(name="Рейд!")
    	for key, value in answers.items():
    		embed.add_field(
    			name=f"Вопрос: `{questionList[key][0]}`",
                value=f"Ответ: `{value}`",
                inline=False)

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
    		await ctx.send("Рейд отменен!")
    		return

    	channelId = re.findall(r"[0-9]+", answers[0])[0]
    	channel = self.bot.get_channel(int(channelId))

    	time = convert(answers[1])

    	RaidEmbed = discord.Embed(
    		title="⚔️ __**Рейд!**__ ⚔️",
    		description=answers[2]
    	)
    	RaidEmbed.set_footer(
    		text=f"Рейд окнчится через {time} секунд, после отправки этого сообщения.")

    	await ctx.send("||@here|| Начало РЕЙДА!")
    	RaidMessage = await channel.send(embed=RaidEmbed)

    	await RaidMessage.add_reaction("⚔️")
    	await RaidMessage.add_reaction("🛡")
    	await RaidMessage.add_reaction("💉")

    	await asyncio.sleep(time)

    	message = await channel.fetch_message(RaidMessage.id)

    	dps = await message.reactions[0].users().flatten()
    	tanks = await message.reactions[1].users().flatten()
    	healers = await message.reactions[2].users().flatten()

    	dps.pop(dps.index(ctx.guild.me))
    	tanks.pop(tanks.index(ctx.guild.me))
    	healers.pop(healers.index(ctx.guild.me))

    	num_dps = len(dps)
    	num_tank = len(tank)
    	num_healer = len(healers)

    	lover = len(dps)+len(tanks)+len(healers)

    	min = 3
    	max = 12

    	with open("Modules/JSONs/rpg.json", "r") as f:
    		users = json.load(f)

    	if  lover < min:
    		await channel.send("Комманда не собралась")
    		return

    	elif lover > max:
    		await channel.send("В рейде максимальное колличество человек")

    	win_num = 0.5

    	if (num_dps or num_tank or num_healer) > 3 and (num_dps or num_tank or num_healer) > (num_tank + num_healer):
    		win_num = 0.4

    		system(win_num, num_dps, num_tank, num_healer, dps, tank, healers)
    		print(system)

    	elif (num_dps or num_tank or num_healer) > 5 and (num_dps or num_tank or num_healer) > (num_tank + num_healer):
    		win_num = 0.3

    		system(win_num, num_dps, num_tank, num_healer, dps, tank, healers)
    		print(system)

    	system(win_num, num_dps, num_tank, num_healer, dps, tank, healers)
    	print(system)
"""

def setup(bot):
    bot.add_cog(Giveaway(bot))
