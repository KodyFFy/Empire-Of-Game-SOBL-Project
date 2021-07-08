import json
import random

import discord
from discord.ext import commands as BOT

import Modules.economy as economy


class Bones(BOT.Cog):
    def __init__(self, Bot):
        self.Bot = Bot

    @BOT.command()
    async def bones(self, ctx, num, amount=None):
        num = int(num)
        user = ctx.author
        await economy.open_account(user)
        users = await economy.get_main_data()
        # await ctx.send("Давайте бросим кубик! 🎲")
        # await ctx.send(file=discord.File("Images/Bones/bone_start.gif"))
        balance = int(users[str(user.id)]["Wallet"])

        if num > 6 or num == "" or num < 1:
            embed = discord.Embed(
                title="Ошибка!",
                description="Ошибка аргумента числа. Возможно вы ввели: "
                            "отрицательное число / ничего / число больше 6 / "
                            "число меньше 1 / текст",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

        else:
            if amount == None:
                randomChoice = random.randint(1, 6)
                num = int(num)
                if num == randomChoice:
                    # name = "bone" +  "_" + str(randomChoice) + ".gif"
                    # await ctx.send(
                    # 	file=discord.File(f"Images/Bones/{name}"))
                    embed = discord.Embed(
                        title="Вы выиграли!",
                        description=f"Кубик 🎲 упал и на нем число {randomChoice}. "
                                     "Вы угадали поздравляю!",
                        color=discord.Color.blurple()
                    )
                    await ctx.send(embed=embed)

                else:
                    # name = "bone" +  "_" + str(ran) + ".gif"
                    # await ctx.send(
                    # 	file=discord.File(f"Images/Bones/{name}"))
                    embed = discord.Embed(
                        title="Вы проиграли!",
                        description=f"Кубик 🎲 упал и на нем число {randomChoice}. "
                                     "Увы, Вы не угадали :(",
                        color=discord.Color.blurple()
                    )
                    await ctx.send(embed=embed)

            else:
                if balance < int(amount):
                    embed = discord.Embed(
                        title="Ошибка!",
                        description="У Вас нет столько денег для игры!",
                        color=discord.Color.red()
                    )
                    await ctx.send(embed=embed)

                else:
                    num = int(num)
                    user = ctx.author

                    await economy.open_account(user)

                    users = await economy.get_main_data()
                    balance = int(users[str(user.id)]["Wallet"])
                    reserv = int(amount)
                    randomChoice = random.randint(1, 6)

                    if num == randomChoice:
                        # name = "bone" +  "_" + str(ran) + ".gif"
                        # await ctx.send(
                        # 	file=discord.File(f"Images/Bones/{name}"))
                        embed = discord.Embed(
                            title="Вы выиграли!",
                            description="Кубик 🎲 упал и  на нем число "
                                       f"{randomChoice}. Вы угадали, "
                                        "поздравляю! "
                                        "Ваш куш - "
                                       f"{reserv + (reserv * 3.5)} "
                                        "<:coin:791004475098660904>",
                            color=discord.Color.blurple()
                        )
                        await ctx.send(embed=embed)

                        users[str(user.id)]["Wallet"] = int(
                            users[str(
                                user.id)]["Wallet"]) + int(
                                    reserv + (reserv * 3.5))

                        with open("JSONs/main.json", "w") as f:
                            json.dump(users, f, indent=4)

                    else:
                        # name = "bone" +  "_" + str(ran) + ".gif"
                        # await ctx.send(
                        # 	file=discord.File(f"Images/Bones/{name}"))
                        embed = discord.Embed(
                            title="Вы проиграли!",
                            description="Кубик 🎲 упал "
                                       f"и на нем число {randomChoice}. "
                                        "Увы вы не угадали :("
                        )
                        await ctx.send(embed=embed)

                        users[str(user.id)]["Wallet"] = int(
                            users[str(user.id)]["Wallet"]
                        ) - reserv

                        with open("JSONs/main.json", "w") as f:
                            json.dump(users, f, indent=4)


def setup(Bot):
    Bot.add_cog(Bones(Bot))
