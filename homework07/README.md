# Asynchronous Programming
The following files were assembled following the lab steps listed [here](https://coe-332-sp21.readthedocs.io/en/main/homework/homework07.html#homework-07s).

## Deploy the Containers:
```bash
$ cd deploy
$ kubectl apply -f ./api
deployment.apps/rry235-hw7-flask-deployment created
service/rry235-hw7-flask-service created
$ kubectl apply -f ./worker
deployment.apps/rry235-hw7-worker-deployment created
$ kubectl apply -f ./db
deployment.apps/rry235-hw7-redis-deployment created
persistentvolumeclaim/rry235-hw7-redis-pvc created
service/rry235-hw7-redis-service created
```
## Verify that the Flask API and worker are working properly:
```bash
root@py-debug-deployment-5cc8cdd65f-dmxw5:/# curl 10.110.202.37:5000/jobs -X POST -d '{"start": "start","end":"end"}'
root@py-debug-deployment-5cc8cdd65f-dmxw5:/# python3
````
```python
>>> import redis
>>> rd = redis.StrictRedis(host='10.100.204.207', port=6379, db=0)
>>> rd.keys()
[b'job.cc4b9a4d-f2b6-4ac7-bd59-120ddd93571b']
>>> print(rd.hmset('job.cc4b9a4d-f2b6-4ac7-bd59-120ddd93571b','status'))
[b'complete']
>>> print(rd.hmset('job.cc4b9a4d-f2b6-4ac7-bd59-120ddd93571b','worker'))
[b'10.244.15.202']
```
## Checking Multiple Created Jobs and Workers who Worked Them:
First, queue 10 more jobs using the syntax shown above. Then, use the following command to check the status of the job and the IP of the worker that worked it. 
```bash
root@py-debug-deployment-5cc8cdd65f-dmxw5:/# curl 10.110.202.37:5000/jobs -X POST -d '{"start": "start","end":"end"}'
{"id": "32999345-f456-455e-9487-9d177deeeec8", "status": "submitted", "start": "start", "end": "end"}
root@py-debug-deployment-5cc8cdd65f-dmxw5:/# curl 10.110.202.37:5000/jobs -X POST -d '{"start": "start","end":"end"}'
{"id": "87cb6a50-c752-462d-b5ed-110f6410c8f3", "status": "submitted", "start": "start", "end": "end"}
root@py-debug-deployment-5cc8cdd65f-dmxw5:/# curl 10.110.202.37:5000/jobs -X POST -d '{"start": "start","end":"end"}'
{"id": "041a981e-157a-45cf-938d-172eea2b586d", "status": "submitted", "start": "start", "end": "end"}
root@py-debug-deployment-5cc8cdd65f-dmxw5:/# curl 10.110.202.37:5000/jobs -X POST -d '{"start": "start","end":"end"}'
{"id": "c993efa0-9e72-4a7d-b642-164f1f67a4a6", "status": "submitted", "start": "start", "end": "end"}
root@py-debug-deployment-5cc8cdd65f-dmxw5:/# curl 10.110.202.37:5000/jobs -X POST -d '{"start": "start","end":"end"}'
{"id": "9023fa2a-f0c1-4391-ad5c-5a4bbb083853", "status": "submitted", "start": "start", "end": "end"}
root@py-debug-deployment-5cc8cdd65f-dmxw5:/# curl 10.110.202.37:5000/jobs -X POST -d '{"start": "start","end":"end"}'
{"id": "8fbeff48-0f06-4ea9-ad80-204f6538ce42", "status": "submitted", "start": "start", "end": "end"}
root@py-debug-deployment-5cc8cdd65f-dmxw5:/# curl 10.110.202.37:5000/jobs -X POST -d '{"start": "start","end":"end"}'
{"id": "15b0525a-0a99-45b8-a96a-0692a3553e04", "status": "submitted", "start": "start", "end": "end"}
root@py-debug-deployment-5cc8cdd65f-dmxw5:/# curl 10.110.202.37:5000/jobs -X POST -d '{"start": "start","end":"end"}'
{"id": "1da41642-977b-41a1-882d-ada20b01dead", "status": "submitted", "start": "start", "end": "end"}
root@py-debug-deployment-5cc8cdd65f-dmxw5:/# curl 10.110.202.37:5000/jobs -X POST -d '{"start": "start","end":"end"}'
{"id": "d339b3bc-b34b-48d1-b634-20e2f37a201a", "status": "submitted", "start": "start", "end": "end"}
root@py-debug-deployment-5cc8cdd65f-dmxw5:/# curl 10.110.202.37:5000/jobs -X POST -d '{"start": "start","end":"end"}'
{"id": "be7a2b4d-62d9-4671-9cdc-0371df7a7846", "status": "submitted", "start": "start", "end": "end"}
```
Next open the python shell and iterate through the databases' keys.
```bash
root@py-debug-deployment-5cc8cdd65f-dmxw5:/# python3
```
```python
>>> import redis
>>> rd = redis.StrictRedis(host='10.100.204.207', port=6379, db=0)
>>> for key in rd.keys():
...     print(rd.hmget(key,'status'))
...     print(rd.hmget(key,'worker'))
...     print()
... 
[b'complete']
[b'10.244.7.182']

[b'complete']
[b'10.244.7.182']

[b'complete']
[b'10.244.15.202']

[b'complete']
[b'10.244.15.202']

[b'complete']
[b'10.244.7.182']

[b'complete']
[b'10.244.15.202']

[b'complete']
[b'10.244.15.202']

[b'complete']
[b'10.244.7.182']

[b'complete']
[b'10.244.15.202']

[b'complete']
[b'10.244.15.202']

[b'complete']
[b'10.244.7.182']

```
The worker with IP address `10.244.7.182` worked 5 jobs while the worker with IP address `10.244.15.202` worked 6 jobs.