# api.py
import json
from flask import Flask, request, jsonify, send_file
import jobs
import redis
import uuid
import datetime
import os
from hotqueue import HotQueue
import datadotworld as dw
import numpy as np

redis_ip = os.environ.get('REDIS_IP')
if not redis_ip:
    raise Exception()


app = Flask(__name__)
rd_data = redis.StrictRedis(host=redis_ip, port=6379, db=0) # data db
rd_jobs = redis.StrictRedis(host=redis_ip, port=6379, db=1) # jobs db
rd_imgs = redis.StrictRedis(host=redis_ip, port=6379, db=3) 
q = HotQueue('queue', host=redis_ip, port=6379, db=2)

@app.route('/', methods=['GET'])
def instructions():
    return """
    This is a test. Hello world.

"""

### Jobs Operations
@app.route('/run', methods=['GET','POST']) # Submits a Job request using POST
# e.g curl localhost:5039/jobs -X POST -d '{"start": "now","end":"later"}'
def run_job():
    if request.method == 'POST':
        try:
            job = request.get_json(force=True)
        except Exception as e:
            return True, json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)})

        return json.dumps(jobs.add_job(str(datetime.datetime.now()),job['min_points'],job['max_points'])) + "\n"
    else:
        return """
    This is a route for POSTing graphing NBA/ABA points scored by state to run. 
    Input a range of points to only plot states whose points fall within the user-inputted range
    Use the form:
    curl -X POST -d '{"min_points": 0.0,"max_points": 200000}' localhost:5039/run
"""

    

@app.route('/jobs/list', methods=['GET']) # Lists past Jobs
def get_jobs():
    redis_dict = {}
    for key in rd_jobs.keys():
        redis_dict[str(key.decode('utf-8'))] = {}
        redis_dict[str(key.decode('utf-8'))]['id'] = rd_jobs.hget(key, 'id').decode('utf-8')
        redis_dict[str(key.decode('utf-8'))]['datetime'] = rd_jobs.hget(key, 'datetime').decode('utf-8')
        redis_dict[str(key.decode('utf-8'))]['status'] = rd_jobs.hget(key, 'status').decode('utf-8')
        redis_dict[str(key.decode('utf-8'))]['min_points'] = rd_jobs.hget(key, 'min_points').decode('utf-8')
        redis_dict[str(key.decode('utf-8'))]['max_points'] = rd_jobs.hget(key, 'max_points').decode('utf-8')
    return json.dumps(redis_dict, indent=4)



@app.route('/download/<jobuuid>', methods=['GET'])
def download(jobuuid):
    path = f'/app/{jobuuid}.png'
    with open(path, 'wb') as f:
        f.write(rd_imgs.hget(jobuuid, 'image'))
    return send_file(path, mimetype='image/png', as_attachment=True)


### Database Operations
@app.route('/players/load_db', methods=['GET']) #load or reset data
def load_data():
    rd_data.flushall()
    with open('player_info.json','r') as f:
	    player_info = json.load(f)
    
    rd_data.set('Player_Info',json.dumps(player_info,indent=2))
    return """===============================================\nPlayer data has been loaded in to the database.\n===============================================\n"""

@app.route('/players/add_player', methods=['POST']) #create player and player_info (CREATE)
# input would be something like:
# curl localhost:5039/players/add_player -X POST -H "Content-Type: application/json" -d '{"player": "Riley Ylagan","pts": "100.0", "city": "Austin", "state": "Texas"}'
# python will generate uuid
def add_player():
    data = get_data()
    new_player_info = request.json
    new_player = new_player_info["player"]
    new_pts = float(new_player_info["pts"])
    new_city = new_player_info["city"]
    new_state = new_player_info["state"]
    data["Players"].append({"Player": new_player,"Pts": new_pts , "City": new_city, "State": new_state,"uuid":str(uuid.uuid4())})
    rd_data.set('Player_Info',json.dumps(data,indent=2))
    return "Player Added\n"

@app.route('/players/get_data', methods=['GET']) #print player data (READ)
def get_player_data():
    data = get_data()
    return jsonify(data)

@app.route('/players/get_data/<uuid>', methods=['GET']) #print player data by ID (READ)
def get_player(uuid):
    data = get_data()
    json_list = data["Players"]
    output = [x for x in json_list if x['uuid'] == uuid]
    return jsonify(output)

@app.route('/players/update_player/<uuid>', methods=['PUT']) #update/change player data (UPDATE)
# curl localhost:5039/players/update_player/14702573-37c0-4318-b597-e6ccd085339c -X PUT -H "Content-Type: application/json" -d '{"player": "Anna Chavez","pts": "200.0", "city": "Scotsdale", "state": "Arizona"}'
def update_player_data(uuid):
    data = get_data()

    new_player_info = request.json
    new_player = new_player_info["player"]
    new_pts = float(new_player_info["pts"])
    new_city = new_player_info["city"]
    new_state = new_player_info["state"]

    index = [index for (index,d) in enumerate(data["Players"]) if d["uuid"] == uuid]
    data["Players"][index[0]]["Player"]= new_player
    data["Players"][index[0]]["Pts"]= new_pts
    data["Players"][index[0]]["City"]= new_city
    data["Players"][index[0]]["State"]= new_state
    rd_data.set('Player_Info',json.dumps(data,indent=2))
    return "Player Updated\n"

@app.route('/players/delete_player/<uuid>', methods=['GET','DELETE']) #delete player (DELETE)
# curl localhost:5039/players/delete_player/78534abf-d442-403e-bb67-358cf239e182
def delete_player(uuid):
    data = get_data()
    index = [index for (index,d) in enumerate(data["Players"]) if d["uuid"] == uuid]
    data["Players"].pop(index[0])
    rd_data.set('Player_Info',json.dumps(data,indent=2))
    return "Player Deleted\n"


def get_data():
	userdata = json.loads(rd_data.get('Player_Info'))
	return userdata


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')