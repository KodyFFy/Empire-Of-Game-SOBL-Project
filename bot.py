import asyncio
import argparse
import logging
import os
import random

import discord
from discord.ext import commands

from config import info


class ArgParser():
    argParser = argparse.ArgumentParser(
            description="Start bot with custom settings")

    argParser.add_argument("--token", type=str,
                           help="Start bot with 'main' or 'test' token",
                           default="test", nargs="?")

    argParser.add_argument("--prefix", type=str,
                           help="Start bot with 'main' or 'test' prefix",
                           default="test", nargs="?")

    parsedArgs = argParser.parse_args()

    if parsedArgs.token == "main":
        token = info["TOKEN_MAIN"]
    elif parsedArgs != "main":
        token = info["TOKEN_TEST"]
    else:
        token = info["TOKEN_TEST"]

    if parsedArgs.prefix == "main":
        pref = info["PREFIX_MAIN"]
    elif parsedArgs.prefix != "main":
        pref = info["PREFIX_TEST"]
    else:
        pref = info["PREFIX_TEST"]


class Logger():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("discord")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(
        filename="Logs/discord.log",
        encoding="utf-8",
        mode="w")

    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s: %(levelname)s: %(name)s: %(message)s"))
    logger.addHandler(handler)


Bot = commands.Bot(command_prefix=ArgParser.pref)


@Bot.event
async def on_ready():
    print(f"Бот успешно запущен!")
Bot.remove_command("help")


@Bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed=discord.Embed(
            title="Ошибка!",
            description=f"Неверный аргумент, попробуйте `{ArgParser.pref}help` "
                         "что-бы узнать больше о командах.",
            color=0xef3417)
        await ctx.send(embed=embed)

    if isinstance(error, commands.CommandNotFound):
        embed=discord.Embed(
            title="Ошибка!",
            description="Такой команды не существует! "
                        "Попробуйте воспользутесь командой "
                       f"`{ArgParser.pref}help`!",
            color=0xef3417)
        await ctx.send(embed=embed)


for module in os.listdir("Modules"):
    _module = os.path.splitext(module)

    if module[0] == "." or module == "__pycache__":
        continue

    else:
        Bot.load_extension("Modules.{0}".format(_module[0]))


@Bot.event
async def change_pings():
    await Bot.wait_until_ready()
    pings = [
        "Пошел делать самогон!", "Хочу прибавку к пенсии!",
        "Ушел ебать соседку Риту!", "Заснул старческим сном... Zzzz",
        "Ждет, когда выведут пенсию...", "Пошел пыхнуть на балкон!",
        "Гоняет лысого...", "Пошел на рыбалку!", "Пошел копать огород!",
        "А вот в наше время...", "Пошел доить корову!",
        "Пошел бухать!", "Отдыхаю на даче!"
    ]

    while not Bot.is_closed():
        ping = random.choice(pings)
        await Bot.change_presence(activity=discord.Game(ping))
        await asyncio.sleep(30)


Bot.loop.create_task(change_pings())
Bot.run(ArgParser.token)
