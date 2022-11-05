import TruliaApiScraper
import pandas as pd
import json
import sqlite3

scrapedJson = TruliaApiScraper.scrapeTrulia()

with open('trulia_data.json','w') as file:
    json.dump(scrapedJson,file,indent=4)
pandasJson = pd.read_json(json.dumps(scrapedJson,indent=4))
df = pd.DataFrame(pandasJson)
df.to_excel("trulia_data.xlsx",header=True)

#connection = sqlite3.connect('real_estate_data.db')
#cursor = connection.cursor
