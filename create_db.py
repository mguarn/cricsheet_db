import load, database
import pandas as pd
import shutil
import os
import yaml



MATCH_TYPE = 't20'
zipurl = 'https://cricsheet.org/downloads/t20s_json.zip'

# Download data from Crichseet
print(f"Downloading data from {zipurl}")
load.download(zipurl=zipurl, folder=MATCH_TYPE)


# Array of files
files = [i for i in os.listdir('data/t20') if not (i.startswith(".") or i == 'README.txt')]

print("Initialising database")
with open('config.yml', 'r') as f:
    db_config = yaml.safe_load(f)['postgres_db']
db = database.init_db(db_config)
database.db.initialize(db)
db.connect()
db.create_tables([database.Match, database.Ball])

print("Storing data in database")
for f in files:
    match, balls = load.events(int(f.split('.')[0]), MATCH_TYPE)
    if match:
        database.Match.insert(match).execute()
    if type(balls) == pd.DataFrame:
        database.Ball.insert_many(balls.to_dict(orient='records')).execute()

db.close()


print("Deleting raw data files")
shutil.rmtree('data/t20')

print("All Done!")