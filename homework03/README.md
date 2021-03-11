# Animal JSON Flask App
The following files create a Flask app that returns animals depending on the parameters read in from the user. To use, flask must be installed. Use:
```bash
$ pip install --user flask
```

## Tools -
- **app.py -** \
This python script allows users to get a set of data from a list of 20 generated animals in the file animals.json using specific routes.\
The flask app has 3 routes: \
    **1. /animals :** \
Prints all animals within the JSON file \
    **2. /animals/head/<type of head> :** \
Prints all animals with the specified type of animal head \
    **3. /animals/legs/<number of legs>** \
Prints all animals with the specified number of legs




## Download -
To download the scripts, clone this folder onto your local device and navigate to where it is located in a terminal. 

## Running the Flask App Outside of a Container -
In the folder containing these files, execute the following commands in the command line:
```bash
$ export FLASK_APP=app.py
$ export FLASK_ENV=development
$ flask run -p 5039
```
Now, in another terminal, you can send requests to the server using curl.\
Example Usage:
```bash
$ curl localhost:5039/animals
$ curl localhost:5039/animals/head/bull
$ curl localhost:5039/animals/legs/6
```

## Running the Flask App with a Container -
To run the Flask app with a container, first build the image:
```bash
$ docker build -t animal_flask_app_rry235:latest .
```
Now run the container:
```bash
$ docker run --name "Animal_Flask_App_rry235" -d -p 5039:5000 animal_flask_app_rry235
```
Now, you can curl the port using the same commands as before:
```bash
$ curl localhost:5039/animals
$ curl localhost:5039/animals/head/bull
$ curl localhost:5039/animals/legs/6
```
## Using the Requestor Script -
The file requestor.py can be used to consume other user's apps. The port and the parameters can be changed using any suitable text editor. To run, use the following command:
```bash
$ python3 requestor.py
```

