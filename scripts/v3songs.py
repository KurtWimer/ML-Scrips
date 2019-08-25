from songs import allSongs

for year in range(2009,2019):
	used = [False] * len(allSongs)
	with open("../data/{}.txt".format(year), "r") as f:
		song = f.readline() #empty line to start file is invalid
		while song != "":
			if song == '\n':
				song = f.readline()
				continue
			try: 
				index = allSongs.index(song.strip('\n'))
				used[index] = True
			except:
				pass
			song = f.readline()
	v3 = list()
	for i in range(len(allSongs)):
		if used[i]:
			v3.append(allSongs[i])
print(v3)
print(len(v3))
