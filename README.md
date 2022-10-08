# Cricsheet_DB

> Create a postgres database using  data from Cricsheet

A project to download ball by ball JSON files from [Cricsheet](https://cricsheet.org/) and store the data in a postgres database. 

Currently it will only download T20 international matches but I plan to update it to handle all the different match types soon.

## How To
1. First clone the repo and change directory to the project
```
git clone https://github.com/mguarn/cricsheet_db.git
cd cricsheet_db
```
2. Copy yaml file and rename to config.yml
```
cp config.sample.yml config.yml
```
3. Fill in config.yml file with database credentials
4. Install requirements
```
pip install -r requirements.txt
```
5. Run create_db.py
```
python create_db.py
```
