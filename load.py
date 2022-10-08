import json
import pandas as pd
from urllib.request import urlopen
from zipfile import ZipFile
from io import BytesIO

def download(zipurl, folder):
    with urlopen(zipurl) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall(f'data/{folder}')

def load_match(match_id, match_type):
    with open(f"data/{match_type}/{match_id}.json", "r") as read_file:
        r = json.load(read_file)
    r['match_id'] = match_id
    return r

def result(match_info):
    if 'winner' in match_info['outcome'].keys():
        return match_info['outcome']['winner']
    else:
        return match_info['outcome']['result']

def event(match_info):
    if 'event' in match_info.keys():
        return match_info['event']['name']
    else:
        return None

def parse_match(match):
    match_info = {}
    info = match['info']

    match_info['id'] = match['match_id']
    match_info['date'] = info['dates'][0]
    match_info['home_team'] = info['teams'][0]
    match_info['away_team'] = info['teams'][1]
    match_info['match_type'] = info['match_type']
    match_info['overs'] = info['overs']
    match_info['event'] = event(info)
    match_info['gender'] = info['gender']
    match_info['result'] = result(info)
    match_info['season'] = info['season']
    match_info['toss_winner'] = info['toss']['winner']
    match_info['toss_decision'] = info['toss']['decision']
    match_info['venue'] = info['venue']
    match_info['version'] = match['meta']['data_version']
    match_info['created_at'] = match['meta']['created']
    return  match_info

def get_fielders(x):
    if type(x) == list:
        return [i['name'] for i in x if 'name' in i.keys()]

def innings_df(innings, batting_team, bowling_team, match_id):
    overs = innings['overs']
    overs_df = []
    for over in overs:
        deliveries = pd.DataFrame(over['deliveries'])
        deliveries['over'] = over['over']
        deliveries['ball'] = deliveries.index + 1
        overs_df.append(deliveries)
    overs_df = pd.concat(overs_df).reset_index(drop=True)

    # Handle runs
    runs = (pd.DataFrame(list(overs_df['runs']))
                .rename(columns={'batter': 'bat_runs', 'total': 'total_runs'}))

    # Handle Extras and wickets
    if 'extras' in overs_df:
        extras = pd.DataFrame(list(overs_df['extras'].dropna()), index=overs_df['extras'].dropna().index)
        overs_df = (overs_df
                    .drop(labels=['runs', 'extras'], axis=1)
                    .join(runs)
                    .join(extras))
    else:
        overs_df.drop(labels=['runs'], axis=1).join(runs)
    # Handle Wickets
    if 'wickets' in overs_df.columns:
        wickets = pd.DataFrame(list(pd.DataFrame(list(overs_df['wickets'].dropna()))[0]),
                            index=overs_df['wickets'].dropna().index).rename(columns={'kind': 'wicket_type'})
        wickets['wicket'] = 1
        if 'fielders' in wickets.columns:
            wickets['fielders'] = wickets['fielders'].apply(get_fielders)
        overs_df = (overs_df
                .drop(labels='wickets', axis=1)
                .join(wickets))

    int_cols = ['over', 'ball', 'bat_runs', 'extras', 'total_runs', 'wides', 'byes', 'legbyes', 'wicket']
    for i in int_cols:
        if i in overs_df.columns:
            overs_df[i] = overs_df[i].fillna(0).astype(int)
        else:
            overs_df[i] = 0

    explicit_cols = ['match_id', 'batting_team', 'bowling_team', 'over', 'ball', 'batter', 'bowler', 'non_striker',
            'total_runs', 'wicket', 'bat_runs', 'extras', 'wides', 'byes', 'legbyes', 'wicket_type', 'player_out',
            'fielders']

    overs_df = (overs_df
                .assign(batting_team=batting_team)
                .assign(bowling_team=bowling_team)
                .assign(match_id=match_id))
    return overs_df[[i for i in explicit_cols if i in overs_df.columns]]


def events(match_id, match_type):
    raw = load_match(match_id, match_type)
    match_df = parse_match(raw)

    innings = raw['innings']
    if len(innings) == 2:
        bat_first = innings[0]['team']
        bat_second = innings[1]['team']

        first = innings_df(innings[0], bat_first, bat_second, match_id).assign(innings=1)
        second = innings_df(innings[1], bat_second, bat_first, match_id).assign(innings=2)
        balls = pd.concat([first, second])

        return match_df, balls
    else:
        print(f"Error loading match {match_id}. {len(innings)} innings.")
        return None, None