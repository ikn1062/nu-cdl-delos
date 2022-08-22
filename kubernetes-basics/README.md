# Kubernetes Basics

## Important Files
1. `client/` contains the necessary files for a client python docker image and pod deployment
   1. `client_py.py` contains the python file to send "Hello World!" and to receive message from server
   2. `client-deployment.yaml` contains the deployment for the python client pod
   3. `Dockerfile` creates the docker image for the client pod
1. `server/` contains the necessary files for a server python docker image and server pod 
   1. `service_py.py` contains the python file to receive "Hello World! from the client and to send "I got it roger!" to the client
   2. `server-deployment.yaml` contains the deployment for the python server pod
   3. `Dockerfile` creates the docker image for the server pod
3. `server-service.yaml` contains the deployment for the service connecting the client to the server

## Running the files

### Overview
The first step in deploying the kubernetes cluster with an interacting client and server is to create
a docker image for the client and server.

The second step is to deploy the `server-service.yaml` kubernetes service, `client-deployment.yaml` pod, 
and the `server-deployment.yaml` pod.

The output can be seen the logs of the client and server deployment.

### Creating Docker Image
If you would like to create a new docker image for this client and server python deployment, follow these steps, 
otherwise, my docker image should still be able to be deployed with the current configuration.

In the client and server folders, where the `Dockerfile`'s are, run the following
```angular2html
cd client
docker build . -t [DOCKER ACCOUNT]/pyclient
cd ..
cd server
docker build . -t [DOCKER ACCOUNT]/pyserver
```

You can then push the file to your docker repository
```angular2html
docker login
docker push [DOCKER ACCOUNT]/pyclient
docker push [DOCKER ACCOUNT]/pyserver
```

If you decide to do this, you need to edit the image in the deployment file. On line 28 of the client yaml
`client-deployment.yaml`, change the image to the following:
```angular2html
image: [DOCKER ACCOUNT]/pyclient
```
Do the same for `server-deployment.yaml` on line 28.

### Editing time lower and time upper
You can edit the time lower and upper for client and server in the `client-deployment.yaml` and `server-deployment.yaml`,
respectively. 

Change the following on lines 9-10 in the files mentioned above:
```
 "TIME_LOWER": 1,
 "TIME_UPPER": 3
```

### Pod and Service Deployment
In a terminal create a kubernetes cluster, cd into this repo and deploy the `server-deployment.yaml`, 
and then deploy the client and server pods.

```angular2html
minikube start
kubectl apply -f server-service.yaml
kubectl apply -f server/server-deployment.yaml
kubectl apply -f client/client-deployment.yaml
```

### Checking File Logs
You can see if the connection between the client and server are working by running the following in 2 seperate terminals:
```angular2html
kubectl logs -f deployment.apps/client-deployment
```

```angular2html
kubectl logs -f deployment.apps/server-deployment
```

