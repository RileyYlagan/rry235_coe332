# -*- coding: utf-8 -*-
import json
from flask import Flask, request, jsonify
import redis
import datetime
import random
import petname
import uuid
import os

app = Flask(__name__)

RD_HOST = os.environ.get('RD_HOST')
RD_PORT = 6379


@app.route('/animals', methods=['GET'])
def get_animals():
	data = get_data()
	json_list = data['animals']
	return jsonify(json_list)

@app.route('/animals/head/<type_head>', methods=['GET'])
def get_animal_head(type_head):
	test = get_data()
	json_list = test['animals']
	output = [x for x in json_list if x['head'] == type_head]
	return jsonify(output)

@app.route('/animals/legs/<num_legs>', methods=['GET'])
def get_animal_legs(num_legs):
	test = get_data()
	json_list = test['animals']
	output = [x for x in json_list if x['legs'] == int(num_legs)]
	return jsonify(output)
# ROUTES FOR MIDTERM
# query a range of dates
@app.route('/animals/dates',methods=['GET'])
def get_dates():
    start = request.args.get('start')
    startdate = datetime.datetime.strptime(start, "'%Y-%m-%d_%H:%M:%S.%f'")
    end = request.args.get('end')
    enddate = datetime.datetime.strptime(end, "'%Y-%m-%d_%H:%M:%S.%f'")
    test = get_data()
    return json.dumps([x for x in test['animals'] if (datetime.datetime.strptime( x['created_on'],'%Y-%m-%d %H:%M:%S.%f') >= startdate and datetime.datetime.strptime( x['created_on'], '%Y-%m-%d %H:%M:%S.%f')<= enddate ) ])

# selects a particular creature by its unique identifier
@app.route('/animals/<uuid>', methods=['GET'])
def get_animal_by_uuid(uuid):
	data = get_data()
	json_list = data['animals']
	output = [x for x in json_list if x['uid'] == uuid]
	return jsonify(output)	

# edits a particular creature by passing the UUID, and updated "stats"
@app.route('/animals/edit_animal')
def put_animal_stats():
	data = get_data()
	rd = redis.StrictRedis(host= RD_HOST, port = RD_PORT, db = 0)
	uid = request.args.get('uid', None)
	arms = request.args.get('arms', None)
	legs = request.args.get('legs', None)
	tails = request.args.get('tails', None)
	index = [index for (index,d) in enumerate(data['animals']) if d['uid'] == uid]
	
	data['animals'][index[0]]['tails'] = int(tails)
	data['animals'][index[0]]['arms'] = int(arms)
	data['animals'][index[0]]['legs'] = int(legs)
	rd.set('animals',json.dumps(data,indent=2))
	return jsonify(data)  

# deletes a selection of animals by a date ranges
@app.route('/animals/delete',methods=['GET'])
def delete_dates():
	start = request.args.get('start')
	startdate = datetime.datetime.strptime(start, "'%Y-%m-%d_%H:%M:%S.%f'")
	end = request.args.get('end')
	enddate = datetime.datetime.strptime(end, "'%Y-%m-%d_%H:%M:%S.%f'")
	data = get_data()
	index = [index for (index,d) in  enumerate(data['animals']) if (datetime.datetime.strptime(d['created_on'],'%Y-%m-%d %H:%M:%S.%f') <= startdate or datetime.datetime.strptime(d['created_on'],'%Y-%m-%d %H:%M:%S.%f') >= enddate)]
	new_data = {}
	new_data['animals'] = []
	for x in index:
		new_data['animals'].append(data['animals'][x])
	
	rd = redis.StrictRedis(host=RD_HOST,port=RD_PORT,db=0)
	rd.set('animals',json.dumps(new_data,indent=2))
	return jsonify(new_data)
# returns the average number of legs per animal
@app.route('/animals/average_num_legs', methods=['GET'])
def get_average_num_legs():
	data = get_data()
	json_list = data['animals']
	count = len(json_list)
	total = 0
	
	for x in json_list:
		total = total + x['legs']

	return str(total/count)
# returns a total count of animals
@app.route('/animals/animal_count', methods=['GET'])
def get_animal_count():
	data = get_data()
	count = len(data['animals'])
	return str(count)

@app.route('/load_data')
def get_load_data():
	data = {}
	data['animals'] = []
	heads = ['snake','bull','lion','raven','bunny']
	for i in range(20):
		num_arms = random.randrange(2,14,2)
		num_legs = random.randrange(3,13,3)
		num_tails = num_arms + num_legs
		data['animals'].append({ 'head': heads[random.randrange(5)], 'body': petname.name()+'-'+petname.name(), 'arms' : num_arms, 'legs': num_legs, 'tails' : num_tails, 'uid' : str(uuid.uuid4()), 'created_on' : '{:%Y-%m-%d %H:%M:%S.%f}'.format(datetime.datetime.now())})
	rd = redis.StrictRedis(host = RD_HOST, port = RD_PORT, db = 0)
	rd.set('animals',json.dumps(data,indent=2))
	return jsonify(data)

#I had an issue with my ssh connection closing while running the server and it kept it running indefinitely
#This was what I used to turn it off
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    
@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

def get_data():
	rd = redis.StrictRedis(host= RD_HOST, port = RD_PORT, db = 0)
	userdata = json.loads(rd.get('animals'))
	return userdata

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
