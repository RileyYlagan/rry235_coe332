import datadotworld as dw
import json
import numpy as np
import uuid

results = dw.query(
	'gmoney/nba-players-birthplaces', 
    'SELECT player,pts,city,state FROM nba_players_by_state ')
df = results.dataframe
df.columns = [x.capitalize() for x in df.columns]
player_info = {}
player_info['Players'] = []
for i in df.index:
    if not(np.isnan(df['Pts'][i])):
        player_info['Players'].append({'Player':df['Player'][i], 'Pts':df['Pts'][i],'City':df['City'][i],'State':df['State'][i],'uuid': str(uuid.uuid4())})

with open('player_info.json','w') as out:
    json.dump(player_info, out, indent=2)

    










