# JSON Generator and Parser

The following set of scripts can generate a JSON of 20 animals and parse the JSON to create a child of two random animals in the list.

## Tools - 
- **generate_animals.py -** \
This script creates 20 bizarre animals utilizing the petname library and writes them into a JSON file designated by the user from the input line.\
Example Usage: 
```console
$ python3 generate_animals.py animals.json
```
- **read_animals.py -** \
This script takes the JSON generated from generate_animals.py, reads two random animals from it, and outputs the child of those two animals.
```console
$ python3 read_animals.py animals.json
```
## How to Download and Run the Scripts - 
To download the scripts, clone this folder onto your local device and navigate to where it is located in a terminal. To run the files you must have python3 installed. Once installed, you can run the scripts as such:
```console
$ python3 generate_animals.py animals.json
$ python3 read_animals.py animals.json
```
## How to Build an Image with the Dockerfile-
To build an image with the Dockerfile, run the following commands:
```console
$ docker build -t <your username>/JSON-parser:1.0 .
```
## How to Run the Scripts Inside a Container (Interactively) -
To run the scripts interactively inside of a container run the following commands:
```console
[local]$ docker run --rm -it <your username>/JSON-parser:1.0 /bin/bash
```
You should now be operating inside of the container. The following should generate the JSON of animals and execute the read script all within the container.
```console
[root /]# cd home
[root home]# generate_animals.py animals.json
[root home]# read_animals.py animals.json
```
## How to Run the Scripts Outside a Container (Non-Interactively) -
To run the scripts non-interactively inside of a container run the following commands:
```console
[local]$ docker run --rm -v $PWD:/data -u $(id -u):$(id -g) <your username>/json-parser:1.0 generate_animals.py /data/animals.json
```
Within the folder you are in, you should see a new file called animals.json appear. To run the read script on it type the following:

```console
[local]$ docker run --rm -v $PWD:/data username/json-parser:1.0 read_animals.py /data/animals.json
```

## How to Run the Unit Test -
To run the unit test, input the following:
```console
$ python3 test_read_animals.py
```
