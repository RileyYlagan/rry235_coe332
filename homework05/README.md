# Kubernetes Exercise
The following files are to be used following the instructions [here](https://coe-332-sp21.readthedocs.io/en/main/homework/homework05.html).
## Part A

### 1. Create the pod by running the following command:
```bash
$ kubectl apply -f partA.yml 
pod/hello created
```
### 2. Get the pod by using the appropriate selector:
```bash
$ kubectl get pods --selector "greeting=personalized"
NAME    READY   STATUS    RESTARTS   AGE
hello   1/1     Running   0          111s
```
### 3. Check the logs of the pod:
```bash
$ kubectl logs hello
Hello, 
```
This is not what we expect as there is no name given as a parameter.
### 4. Delete the pod using the following command:
```bash
$ kubectl delete pods hello
pod "hello" deleted
```
## Part B 

### 1. Create the pod by running the following command:
```bash
$ kubectl apply -f partB.yml 
pod/hello created
```

### 2. Check the logs of the pod:
```bash
$ kubectl logs hello
Hello, Riley
```

### 3. Delete the pod using the following command:
```bash
$ kubectl delete pods hello
pod "hello" deleted
```

## Part C 

### 1. Create the pod by running the following command:
```bash
$ kubectl apply -f partB.yml 
deployment.apps/hello-deployment created
```

### 2. Get all of the pods in the deployment:
```bash
$ kubectl get pods --output=wide
NAME                                READY   STATUS    RESTARTS   AGE     IP             NODE   NOMINATED NODE   READINESS GATES
hello-deployment-64565cc4db-476jk   1/1     Running   0          6m26s   10.244.3.197   c01    <none>           <none>
hello-deployment-64565cc4db-pq9hx   1/1     Running   0          6m26s   10.244.5.136   c04    <none>           <none>
hello-deployment-64565cc4db-rlprf   1/1     Running   0          6m26s   10.244.4.155   c02    <none>           <none>
```

### 3. Check the logs of each pod in the deployment:
```bash
$ kubectl logs hello-deployment-64565cc4db-476jk
Hello, Riley from IP 10.244.3.197

$ kubectl logs hello-deployment-64565cc4db-pq9hx 
Hello, Riley from IP 10.244.5.136

$ kubectl logs hello-deployment-64565cc4db-rlprf
Hello, Riley from IP 10.244.4.155
```
The IPs of each pod match those shown above. 