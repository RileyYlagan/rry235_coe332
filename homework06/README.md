# Deploying our Flask APIs to Kubernetes
The following files were assembled following the lab steps listed [here](https://coe-332-sp21.readthedocs.io/en/main/week10/services.html#homework-6-deploying-our-flask-api-to-k8s).
## How to Launch the Application -
### Start the Services
```bash
$ kubectl apply -f rry235-test-flask-service.yml
service/rry235-test-flask-service created

$ kubectl apply -f rry235-test-redis-service.yml
service/rry235-test-redis-service created
```
### Change the Host IP -
##### The IP of the redis service is different every time the service is created and ran. You must change the RD_HOST environment value in rry235-test-flask-deployment to the IP of your service.
#### Check services and copy the IP of the redis service:
```bash
$ kubectl get services
NAME                        TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
rry235-test-flask-service   ClusterIP   10.99.60.135   <none>        5000/TCP   7s
rry235-test-redis-service   ClusterIP   10.99.18.166   <none>        6379/TCP   12s
```
#### Change the value of RD_HOST in app.py to the IP from above. In this case it would be `10.99.18.166`.

```bash
$ cd web
$ vim app.py
```
### Start the Deployments - 
```bash
$ kubectl apply -f rry235-test-flask-deployment.yml 
deployment.apps/rry235-test-flask-deployment created

$ kubectl apply -f rry235-test-redis-deployment.yml 
deployment.apps/rry235-test-redis-deployment created

$ kubectl apply -f python-debug.yml 
deployment.apps/py-debug-deployment created
```

### Check Pods - 
```bash
$ kubectl get pods
NAME                                            READY   STATUS    RESTARTS   AGE
py-debug-deployment-5cc8cdd65f-6wb6h            1/1     Running   0          38s
rry235-test-flask-deployment-765ffd589f-4qzq9   1/1     Running   0          38s
rry235-test-flask-deployment-765ffd589f-vrtwm   1/1     Running   0          38s
rry235-test-redis-deployment-84c5f4d747-hg8hl   1/1     Running   0          38s
```

## Using the Application Within the Python Debug Shell - 
### Exec into the Python Debug Container - 
```bash
$ kubectl exec -it py-debug-deployment-5cc8cdd65f-6wb6h -- /bin/bash
root@py-debug-deployment-5cc8cdd65f-6wb6h:/#
```
### Install redis and curl - 
```bash
root@py-debug-deployment-5cc8cdd65f-6wb6h:/# pip install redis
root@py-debug-deployment-5cc8cdd65f-6wb6h:/#apt-get update && apt-get install -y curl
```
### Curl the IP of you flask service from above and use the routes - 
```bash
root@py-debug-deployment-5cc8cdd65f-6wb6h:/# curl 10.99.60.135:5000/load_data
{
  "animals": [
    {
      "arms": 6, 
      "body": "gar-colt", 
      "created_on": "2021-04-14 01:25:55.190918", 
      "head": "bull", 
      "legs": 6, 
      "tails": 12, 
      "uid": "39cb059d-f6b5-46cb-b470-b6fc8ef778c8"
    }, 
    ...
```
Documentation for the routes can be found in the README of the midterm [here](https://github.com/RileyYlagan/rry235_coe332/tree/main/midterm).
