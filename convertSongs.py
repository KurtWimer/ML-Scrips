from songs import allSongs

def convert(fileName):
	cover = len(allSongs) #let a cover be represented by an int one after all songs
	out = list()
	with open(fileName, "r") as f:
		song = f.readline() #empty line to start file is invalid
		while song != "":
			if song == '\n':
				song = f.readline()
				continue
			try: 
				index = allSongs.index(song.strip('\n'))
				out.append(index)
			except: #not found in allSongs
				print(song)
				out.append(cover)
			song = f.readline()
		return out
	return None #failed to open

if __name__=="__main__":
	print(convert("songData.txt"))