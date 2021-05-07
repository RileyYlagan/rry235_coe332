# Final Project - NBA/ABA Players by Birthplace
This repository follows the requirements [here](https://coe-332-sp21.readthedocs.io/en/main/homework/final_project.html). The dataset is comprised of NBA/ABA player and their city, state, and points scored in the league up until 2017. The dataset in `.json` format can be found in `/src` .

## Deployment of the Systems - 
The system is deployed on a Kubernetes cluster. To deploy the system, run the `k-prod` target in the Makefile.
```bash
[isp]$ make k-prod
cat kubernetes/prod/* | TAG="0.1.0" envsubst '${TAG}' | yq | kubectl apply -f -
deployment.apps/rry235final-prod-api-deployment created
service/rry235final-prod-api-service created
deployment.apps/rry235final-prod-db-deployment created
persistentvolumeclaim/rry235final-prod-db-pvc created
service/rry235final-prod-db-service created
deployment.apps/rry235final-prod-wrk-deployment created
```
The services, deployments, and persistent volume claim should all be created. You can check by running `kubectl get services`, `kubectl get deployments`, `kubectl get pvc`. Running `make k-prod-del` will delete all the deployments if needed. 

Similarly, this can be done with the Kubernetes test environment located in `/kubernetes/test`. Instead run `make k-test` and `make k-test-del`

<b>Note:</b> The value of the environment variable `REDIS_IP` located `rry235-final-prod-api-deployment` and `rry235-final-prod-wrk-deployment`  in must match the IP of the database service. If needed, edit the value of it accordingly. The IP of the API service will be used to curl your routes later on. 

## User Documentation - 
One way to interact with the API is through curling routes in a python-debug container. The following examples are shown using this method.

### <u>The API contains the following routes</u>:
### Database Routes:
#### <b>/players/load_db </b>
- Loads or resets the database. Uses a GET request.
- This should always be done first when using the API.
- Example usage: 
    ```bash
    root@py-debug-deployment-5cc8cdd65f-dmxw5:/# curl 10.101.174.55:5000/players/load_db
    ===============================================
    Player data has been loaded in to the database.
    ===============================================
    ```
#### <b>/players/get_data </b>
- Returns the entire database in JSON format. Uses a GET request.
- Example usage: 
    ```bash
    root@py-debug-deployment-5cc8cdd65f-dmxw5:/# curl 10.101.174.55:5000/players/get_data
    {
  "Players": [
    {
        "City": "Birmingham", 
        "Player": "Michael Ansley", 
        "Pts": 1026.0, 
        "State": "Alabama", 
        "uuid": "3b6e471d-2a3b-4acf-84bb-92e1aeed8f59"
    },
    ...
    ```
#### <b>/players/get_data/< uuid > </b>
- Returns a player with the given uuid. Uses a GET request.
- Example usage: 
    ```bash
    root@py-debug-deployment-5cc8cdd65f-dmxw5:/# curl 10.101.174.55:5000/players/get_data/3b6e471d-2a3b-4acf-84bb-92e1aeed8f59
    {
    "City": "Birmingham", 
    "Player": "Michael Ansley", 
    "Pts": 1026.0, 
    "State": "Alabama", 
    "uuid": "3b6e471d-2a3b-4acf-84bb-92e1aeed8f59"
    }
    ```
#### <b>/players/add_player </b>
- Adds a player to the database. Uses a POST request.
- Uses format `curl 10.101.174.55:5000/players/add_player -X POST -H "Content-Type: application/json" -d '{"player": "Name","pts": "points", "city": "city", "state": "state"}'`
- Example usage: 
    ```bash
    root@py-debug-deployment-5cc8cdd65f-dmxw5:/# curl 10.101.174.55:5000/players/add_player -X POST -H "Content-Type: application/json" -d '{"player": "Bevo","pts": "40.0", "city": "Austin", "state": "Texas"}'
    Player Added
    ```

#### <b>/players/delete_player/< uuid > </b>
- Deletes a player by uuid.
- Example usage: 
    ```bash
    root@py-debug-deployment-5cc8cdd65f-dmxw5:/# curl 10.101.174.55:5000/players/delete_player/3b6e471d-2a3b-4acf-84bb-92e1aeed8f59
    Player Deleted

    root@py-debug-deployment-5cc8cdd65f-dmxw5:/# curl 10.101.174.55:5000/players/get_data/3b6e471d-2a3b-4acf-84bb-92e1aeed8f59
    []
    ```

#### <b>/players/update_player/< uuid > </b>
- Updates a player's information by given uuid. Uses a POST request.
- Example usage: 
    ```bash
    root@py-debug-deployment-5cc8cdd65f-dmxw5:/# curl 10.101.174.55:5000/players/get_data/97d243f1-5e6a-4569-8d8c-44374277ea40
    [
    {
        "City": "Athens", 
        "Player": "Keith Askins", 
        "Pts": 1852.0, 
        "State": "Alabama", 
        "uuid": "97d243f1-5e6a-4569-8d8c-44374277ea40"
    }
    ]

    root@py-debug-deployment-5cc8cdd65f-dmxw5:/#  curl 10.101.174.55:5000/players/update_player/97d243f1-5e6a-4569-8d8c-44374277ea40 -X PUT -H "Content-Type: application/json" -d '{"player": "John Doe","pts": 200.0, "city": "Scotsdale", "state": "Arizona"}'
    Player Updated

    root@py-debug-deployment-5cc8cdd65f-dmxw5:/# curl 10.101.174.55:5000/players/get_data/97d243f1-5e6a-4569-8d8c-44374277ea40
    [
    {
        "City": "Scotsdale", 
        "Player": "John Doe", 
        "Pts": 200.0, 
        "State": "Arizona", 
        "uuid": "97d243f1-5e6a-4569-8d8c-44374277ea40"
    }
    ]
    ```

## Job Routes:
#### <b>/run </b>  
- Submits a job using a POST request.
- The job sums up the total points scored by players born in each state and graphs the result in descending order.
- Example usage:
    ```bash
    root@py-debug-deployment-5cc8cdd65f-dmxw5:/# curl -X POST -d '{"min_points": 200000,"max_points": 1000000}' 10.101.174.55:5000/run
    {"id": "e6c34728-90c6-4dc3-aae5-4899af442605", "status": "submitted", "datetime": "2021-05-06 20:31:05.549055", "min_points": 200000, "max_points": 1000000}
    ``` 

#### <b>/jobs/list </b>  
- Returns a list of previous jobs and their id, datetime, status, and minimum and maximum points input.
- Example usage:
    ```bash
    root@py-debug-deployment-5cc8cdd65f-dmxw5:/# curl 10.101.174.55:5000/jobs/list
    {
        "job.e6c34728-90c6-4dc3-aae5-4899af442605": {
            "id": "e6c34728-90c6-4dc3-aae5-4899af442605",
            "datetime": "2021-05-06 20:31:05.549055",
            "status": "complete",
            "min_points": "200000",
            "max_points": "1000000"
        }
    }
    ``` 
#### <b>/download/< jobuuid > </b>  
- Downloads the image created by the job whose id is taken in as input.
- Example usage:
    ```bash
    root@py-debug-deployment-5cc8cdd65f-dmxw5:/# curl 10.101.174.55:5000/download/e6c34728-90c6-4dc3-aae5-4899af442605 > output.png
    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                    Dload  Upload   Total   Spent    Left  Speed
    100  115k  100  115k    0     0  6411k      0 --:--:-- --:--:-- --:--:-- 6788k

    root@py-debug-deployment-5cc8cdd65f-dmxw5:/# ls
    bin  boot  dev  etc  home  lib  lib64  media  mnt  opt output.png proc  root  run  sbin  srv  sys  tmp  usr  var
    ``` 
- This example will put the image into output.png in your container. This can be copied onto your device use `kubectl cp`

Another way to interact with the API is through an outside NodePort service. Navigate to `https://isp-proxy.tacc.utexas.edu/rry235/ ` which can be used to print information and download the image. For this, run the job in the python -debug container, then list the job in the browser and use the output to get the id to download the image from the job. 



