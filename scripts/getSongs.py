import http.client
import json
import datetime
import re
import time
from bs4 import BeautifulSoup

apiKey = "2603A36D4CDA60A0BD3A"
payload = ""

def getSetlist(showid):
	try:
		#get the data
		conn = http.client.HTTPSConnection("api.phish.net")
		conn.request("GET", "/v3/setlists/get?apikey={}&showid={}".format(apiKey, showid), payload)
		res = conn.getresponse()
		data = json.loads(res.read())
		year = int(data["response"]["data"][0]["showdate"][0:4])
		month = int(data["response"]["data"][0]["showdate"][5:7])
		day = int(data["response"]["data"][0]["showdate"][8:10])
		date = datetime.datetime(year, month, day)
		soup = BeautifulSoup(data["response"]["data"][0]["setlistdata"], features="html5lib")
		
		# remove any instance of [_]
		text = re.sub(r"\[.\]","",soup.get_text())
		# remove set tags
		text = re.sub(r"Unfinished","",text)
		# split by songs
		songs = re.split("->|>|,|Set [0-9]:|Encore:|Encore [0-9]:", text)
		for i in range(len(songs)):
			#remove trailing trash data from songs
			#possibly can favor a combination that drops the song out
			pattern = re.compile("^(.*)(Trey|;|Sung|Lyrics|Performed|Phish|No intro|Debut|Page|Mike|No W|No \"|No w|lyrics)(.*)$")
			match = pattern.search(songs[i])
			if(match != None):
				songs[i] = match.group(1)
			songs[i] = songs[i].strip(".")
			songs[i] = songs[i].strip()
			if songs[i] == "My Friend": #"My Friend, My Friend" get improperly split
				songs[i] = "My Friend, My Friend"
				songs[i+1] = ""
		try: 
			shows.remove(0)#empty first element
			shows.remove(shows.index("0.0"))#will only remove one but i believe only one shows up per setlist anyways
		except:
			pass #thats fine we didn't find '0.0'
		return date, songs
	except:
		print("ERROR showID {}".format(showid))
		return datetime.datetime.now(), list()


#todo this is returning same regardless of year
#gets all Phish show id's for a given year
def getShowIds(year):
	conn = http.client.HTTPSConnection("api.phish.net")
	conn.request("POST", "/v3/shows/query?apikey={}&year={}".format(apiKey, year))
	res = conn.getresponse()
	data = json.loads(res.read().decode("utf-8"))["response"]["data"]
	shows = list()
	#for each show
	for i in range(len(data)):
		artistid = data[i]["artistid"]
		if artistid != 1:
			continue
		shows.append(data[i]["showid"])
	return shows

def main():
	for year in range(2009,2019):
		shows = getShowIds(year)
		l = list()
		for showid in shows:
			try:
				date, songs = getSetlist(showid)
				l.append((date,songs))
			except:
				pass # getSetlist responded with no data
					 # seems to be some inconsistancies in livePhish's db
		sortedSets = sorted(l, key = lambda d: l[0])
		with open("data/{}.txt".format(year), "w") as f:
			for setlist in sortedSets:
				songs = setlist[1]
				for song in songs:
					print(song, file=f)
		print("Done {}".format(year))
		time.sleep(50) #make sure not to exceed api limits, probobly unneccesary


if __name__=="__main__":
	main()
