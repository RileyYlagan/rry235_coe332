import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/animals', methods=['GET'])
def get_animals():
	return json.dumps(get_data())

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
	with open("animals.json","r") as json_file:
		userdata = json.load(json_file)
	return userdata

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
