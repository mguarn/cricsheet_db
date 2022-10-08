import peewee as pw

db = pw.DatabaseProxy()

def init_db(config):
    return pw.PostgresqlDatabase(config['database'],
                                 user=config['username'],
                                 password=config['password'],
                                 host=config['host'],
                                 port=config['port'])

class Match(pw.Model):
    id = pw.PrimaryKeyField()
    date = pw.DateField()
    home_team = pw.TextField()
    away_team = pw.TextField()
    match_type = pw.TextField()
    overs = pw.IntegerField()
    event = pw.TextField(null=True)
    gender = pw.TextField()
    result = pw.TextField()
    season = pw.TextField()
    toss_winner = pw.TextField()
    toss_decision = pw.TextField()
    venue = pw.TextField()
    version = pw.TextField()
    created_at = pw.DateField()
    class Meta:
        database = db
        table_name = 'matches'

class Ball(pw.Model):
    id = pw.PrimaryKeyField()
    match_id = pw.ForeignKeyField(Match)
    batting_team = pw.TextField()
    bowling_team = pw.TextField()
    over = pw.IntegerField()
    ball = pw.IntegerField()
    batter = pw.TextField()
    bowler = pw.TextField()
    non_striker = pw.TextField()
    total_runs = pw.IntegerField()
    wicket = pw.BooleanField()
    bat_runs = pw.IntegerField()
    extras = pw.IntegerField()
    wides = pw.IntegerField()
    byes = pw.IntegerField()
    legbyes = pw.IntegerField()
    wicket_type = pw.TextField(null=True)
    player_out = pw.TextField(null=True)
    fielders = pw.TextField(null=True)
    innings = pw.IntegerField()
    class Meta:
        database = db
        table_name = 'balls'
