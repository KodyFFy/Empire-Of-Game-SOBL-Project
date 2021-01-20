# import random
# import asyncio
# import json



# async def system(win_num, num_dps, num_tank, num_healer, dps, tank, healer):

# 	wins = 0

# 	with open("Modules/jsons/rpg.json", "r") as f:
# 		users = json.load(f)

# 	for i in range(num_dps):
# 		player = dps[i]
# 		lvl = users[str(player.id)]["Skills"]["DPS"]

# 		end_win = lvl * win_num
# 		wins += end_win
# 	for i in range(num_tank):
# 		player = tank[i]
# 		lvl = users[str(player.id)]["Skills"]["TANK"]

# 		end_win = lvl * win_num
# 		wins += end_win
# 	for i in range(num_healer):
# 		player = healer[i]
# 		lvl = users[str(player.id)]["Skills"]["HEALERS"]

# 		end_win = lvl * win_num
# 		wins += end_win

# 	k = random.uniform(2,3.3)

# 	k = round(k,1)


# 	ends_win = wins * k
# 	return ends_win
