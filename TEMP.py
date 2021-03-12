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
		
			await channel.send(f"**{ctx.author.mention} VS {member.mention}|**")
			await channel.send("__**Добро пожаловать в игру: Крестики-Нолики!**__")
			await channel.send("Вы можете поставить ставку на свою победу. Победитель забирает __**ВСЕ!!!**__ .")
			await channel.send("__В случае отказа проигравшего отдать ставку, вы можете к администрации для получения вознаграждения за победу. Незабудьте про пруфы.__")


