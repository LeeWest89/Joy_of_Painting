import csv
import json

episode = 'episode.csv'
episodeData = 'episodeData.json'

# Read CSV
data = []
with open(episode, 'r', encoding='utf-8') as csv_f:
  csv_reader = csv.DictReader(csv_f)
  for row in csv_reader:
    data.append(dict(row))

# Write Json
with open(episodeData, 'w', encoding='utf-8') as json_f:
  json.dump(data, json_f, indent=4)

print(f"CSV file '{episode}' has been converted to JSON file '{episodeData}'.")