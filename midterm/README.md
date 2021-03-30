# Flask and Redis Container Orchestration

This program is an extension of the Flask app from `homework03` with the Redis database.

## Installation -  
To run the program, clone this repository onto your local device and navigate to the `midterm` folder on your local device.

## Containerizing the Flask App and Redis Database - 
Create and run the container using `docker-compose`: 
```bash
$ docker-compose up -d
```
When you initially start the container,the Redis database will be empty, so you must populate it using the `/load_data` route
```bash
$ curl localhost:5039/load_data
```
When you are finished with the container, close it using `docker-compose down`

## Tools -

### /load_data
Generates a random set of 20 animals to use.
```bash
$ curl localhost:5039/load_data
```

### /animals/dates
Returns all animals created between a `start` date and an `end` date.
```bash
$ curl "localhost:5039/animals/dates?start='2021-03-28_22:02:30.99000'&end='2021-03-29_22:02:50.994542'" 
```

### /animals/<uuid>
Returns the animal with the corresponding unique identifier.
```bash
$ curl localhost:5039/animals/e75936c9-c1c0-4baf-9f70-6dec06448702
```


### /animals/edit_animal
Pass in a unique identifier and change the stats of that animal.
```bash
$ curl "localhost:5039/animals/edit_animal?uid=4d343d17-c7b0-477a-98ea-d61209313277&legs=12&tails=4&arms=5"
```

### /animals/delete
Deletes all animals between the `start` date and `end` date.
```bash
$ curl "localhost:5039/animals/delete?start='2021-03-28_22:02:30.99000'&end='2021-03-29_22:02:50.994542'" 
```

### /animals/average_num_legs
Returns the average number of legs of the database of animals.
```bash
$ curl localhost:5039/animals/average_num_legs 
```

### /animals/animal_count
Returns the number of animals in the database.
```bash
$ curl localhost:5039/animals/animal_count
```

