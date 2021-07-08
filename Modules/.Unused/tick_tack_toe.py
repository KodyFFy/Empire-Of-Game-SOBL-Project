import asyncio
import json

import discord
from discord.ext import commands as BOT

from config import botInfo
from Imports.util import GetMessage


class TickTakToe(BOT.Cog):

    def __init__(self, Bot):
        self.Bot = Bot

    @BOT.command()
    async def stavka(self, ctx, amount):
        with open("JSONs/main.json", "r") as f:
            users = json.load(f)

        bal = [users[str(user.id)]["Wallet"], users[str(user.id)]["Bank"]]

        if bal[0] < amount:
            await ctx.send("У вас нет столько денег в кошельке")
        else:

            bal[0] -= amount

            await ctx.send(f"{amount} успешно зарезервированны для игры!")
            rezerv = amount

            with open("Modules/JSONs/reserv.json", "w") as f:
                users = json.load(f)

    @BOT.command()
    async def ttt(self, ctx, member: discord.Member = None):
        if member == None:
            await ctx.send("Вы не выбрали противника")

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



            emj = ['0️⃣','1️⃣', '2️⃣', '3️⃣', '4️⃣','5️⃣', '6️⃣', '#️⃣', '✅', '❌']

            embed=discord.Embed(
                title="Сделать ставку",
                color=discord.Colour.gold(),
                timestamp=ctx.message.created_at)
            embed.add_field(
                name="Ставки",
                value="0️⃣ - 0 💰, 1️⃣ - 50 💰, 2️⃣ - 150 💰, "
                      "3️⃣ - 200 💰, 4️⃣ - 500 💰",
                inline=False)
            embed.add_field(name="Ставки",
                value="5️⃣ - 1000 💰, 6️⃣ - 5000 💰, "
                      "#️⃣ - Ва-банк 💰, ✅ - старт, ❌ - отказаться от игры",
                inline=True)
            embed.set_footer(
                text=f'{guild.me} создал опрос',
                icon_url=guild.me.avatar_url)
            msg = await channel.send("__**||@here||**__\n__**Добро пожаловать "
                                     "в игру: Крестики-Нолики!**__\nЕсли вы "
                                     "хотите сделать ставку нажав на эмодзи "
                                     "с номером",
                                     embed=embed)

            for i in range(len(emj)):
                await msg.add_reaction(emj[i])

            with open("JSONs/ttt_roles.json", "r") as f:
                ids = json.load(f)

            idsss = msg.id
            ids[idsss] = {}
            ids[idsss]["id"] = idsss

            with open("JSONs/ttt_roles.json", "w") as j:
                json.dump(ids, j, indent = 4)

    #@BOT.Cog.listener
    #async def on_raw_reaction_add(payload):

def setup(Bot):
    Bot.add_cog(TickTakToe(Bot))
