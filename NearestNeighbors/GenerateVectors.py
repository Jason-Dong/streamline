import csv
with open("spotifysongs.csv", "r") as f:
	spotifyIDs = list(csv.reader(f, delimiter=';'))
	print(spotifyIDs)
