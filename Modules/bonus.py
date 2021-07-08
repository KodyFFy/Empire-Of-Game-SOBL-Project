import asyncio
import json
import random

import discord
from bot import ArgParser
from discord.ext import commands as BOT

import Modules.economy as economy

wait_bonus = []


class Bonus(BOT.Cog):
    def __init__(self, Bot):
        self.Bot = Bot

    @BOT.command()
    async def bonus(self, ctx):
        embed = discord.Embed(
            title="Информация",
            description="Для получения бонуса перейдите по ссылке и разрешите "
                       f"уведомление! Потом пропишите {ArgParser.pref}use "
                        "(**ваш код**)\nНажимая разрешить уведомления "
                        "при переходе, вы помогаете серверу\n"
                        "Ссылка >>> https://goo.su/EOG_PROMO\n"
                        "Документация по удалению уведомления из вашего "
                        "браузера >>> https://goo.su/41kZ\n",
            color=discord.Color.blurple()
        )
        await ctx.send(embed=embed)

    @BOT.command()
    @BOT.has_permissions(administrator=True)
    async def createpromo(self, ctx, promoCode, activates):
        with open("JSONs/promos.json", "r") as f:
            promoCodes = json.load(f)

        if str(promoCode) in promoCodes:
            await ctx.send(
               f"Такой промокод уже есть, чтобы изменить его "
                "удалите его и снова создайте. Вы можете "
                "узнать о промокодах и инфу о них "
               f"с помощью {ArgParser.pref}listpromo"
            )

        else:
            if int(activates) == 0:
                embed = discord.Embed(
                    title="Готово!",
                    description="Промокод с бесконечным количеством "
                                "использования, успешно создан!",
                    color=discord.Color.blurple()
                )
                await ctx.send(embed=embed)

                promoCode = str(promoCode)

                with open("JSONs/promos.json", "r") as f:
                    promoCodes = json.load(f)

                    promoCodes[promoCode] = {}
                    promoCodes[promoCode][promoCode] = promoCode
                    promoCodes[promoCode][promoCode] = {}
                    promoCodes[promoCode][promoCode]["Options"] = {}
                    promoCodes[promoCode][promoCode]["Options"]["Use"] = activates

            elif int(activates) < 0:
                embed = discord.Embed(
                    title="Готово!",
                    descriprion="Количество активаций должно быть "
                                "неотрицательным **числом**",
                    color=discord.Color.blurple
                )
                await ctx.send(embed=embed)

            else:
                embed = discord.Embed(
                    title="Готово!",
                    description=f"Промокод c {activates} использованиями, "
                                 "успешно создан!",
                    color=discord.Color.blurple()
                )
                await ctx.send(embed=embed)

                promoCode = str(promoCode)
                with open("JSONs/promos.json", "r") as f:
                    promoCodes = json.load(f)

                    promoCodes[promoCode] = {}
                    promoCodes[promoCode][promoCode] = promoCode
                    promoCodes[promoCode][promoCode] = {}
                    promoCodes[promoCode][promoCode]["Options"] = {}
                    promoCodes[promoCode][promoCode]["Options"]["Use"] = activates

        with open("JSONs/promos.json", "w") as f:
            json.dump(promoCodes, f, indent=4)

    @BOT.command()
    @BOT.has_permissions(administrator=True)
    async def delpromo(self, ctx, promoCode):
        with open("JSONs/promos.json", "r") as f:
            promoCodes = json.load(f)

        if str(promoCode) in promoCodes:
            del promoCodes[promoCode]
            embed = discord.Embed(
                title="Готово!",
                description="Промокод был успешно удалён!",
                color=discord.Color.blurple()
            )
            await ctx.send(embed=embed)

            with open("JSONs/promos.json", "w") as f:
                json.dump(promoCodes, f, indent=4)

        else:
            embed = discord.Embed(
                title="Ошибка!",
                description="Такого промокода нет "
                            "или вы неправильно его указали!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @BOT.command()
    @BOT.has_permissions(administrator=True)
    async def listpromo(self, ctx):
        with open("JSONs/promos.json", "r") as f:
            promoCodes = json.load(f)

        embed = discord.Embed(
            title="Все промокоды",
            color=discord.Color.blurple()
        )

        for i in promoCodes:
            activates = promoCodes[i][i]["Options"]["Use"]
            embed.add_field(
                name=f"Промокод ==> {i}",
                value=f"Количество использований ==> {activates}, "
                       "Если количество использований 0, то неограниченно"
            )
        await ctx.send("Информация о промокодах", embed=embed)

    @BOT.command()
    async def promouse(self, ctx, promo):
        with open("JSONs/promos.json", "r") as f:
            promoCodes = json.load(f)

        if not str(ctx.author.id) in wait_bonus:
            for i in promoCodes:
                if promo == i:
                    activates = promoCodes[i][i]["Options"]["Use"]
                    if activates == 0:
                        user = ctx.author
                        await economy.open_account(user)

                        users = await economy.get_main_data()
                        balance = int(users[str(user.id)]["Bank"])

                        get = random.randint(250, 4500)

                        users[str(user.id)]["Bank"] += get

                        embed = discord.Embed(
                            title="Готово!",
                            description="Промокод успешно активирован!",
                            color=discord.Color.blurple()
                        )
                        await ctx.send(embed=embed)

                        with open("JSONs/main.json", "w") as f:
                            json.dump(users, f, indent=4)

                        wait_bonus.append(str(ctx.author.id))

                    elif activates == 1:
                        promoCodes[i][i]["Options"]["Use"] = -1
                        user = ctx.author
                        await economy.open_account(user)

                        users = await economy.get_main_data()
                        balance = int(users[str(user.id)]["Bank"])

                        get = random.randint(250, 4500)

                        users[str(user.id)]["Bank"] += get

                        embed = discord.Embed(
                            title="Готово!",
                            description="Промокод успешно активирован!",
                            color=discord.Color.blurple()
                        )
                        await ctx.send(embed=embed)

                        with open("JSONs/main.json", "w") as f:
                            json.dump(users, f, indent=4)

                        wait_bonus.append(str(ctx.author.id))

                    elif activates == -1:
                        embed = discord.Embed(
                            title="Ошибка!",
                            description="Промокад истёк ;~;",
                            color=discord.Color.red()
                        )
                        await ctx.send(embed=embed)

                    else:
                        activates = int(promoCodes[i][i]["Options"]["Use"])
                        activates -= 1
                        promoCodes[i][i]["Options"]["Use"] = activates
                        user = ctx.author
                        await economy.open_account(user)

                        users = await economy.get_main_data()
                        balance = int(users[str(user.id)]["Bank"])

                        get = random.randint(250, 4500)

                        users[str(user.id)]["Bank"] += get

                        embed = discord.Embed(
                            title="Готово!",
                            description="Промокод успешно активирован!",
                            color=discord.Color.blurple()
                        )
                        await ctx.send(embed=embed)

                        with open("JSONs/main.json", "w") as f:
                            json.dump(users, f, indent=4)

                        wait_bonus.append(str(ctx.author.id))

            if not promo in promoCodes:
                embed = discord.Embed(
                    title="Ошибка!",
                    description="Такого промокода нет :(",
                    color=discord.Color.blurple()
                )
                await ctx.send(embed=embed)

            with open("JSONs/promos.json", "w") as f:
                json.dump(promoCodes, f, indent=4)

            await asyncio.sleep(24 * 60 * 60)
            wait_beg.remove(str(ctx.author.id))

        else:
            embed = discord.Embed(
                title="Ошибка!",
                description="Вы сегодня уже использовали промокод! "
                            "Приходите завтра!",
                color=discord.Color.blurple()
            )
            await ctx.send(embed=embed)


def setup(Bot):
    Bot.add_cog(Bonus(Bot))
