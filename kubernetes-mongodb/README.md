# Kubernetes Mongo

## Important Files
1. `mongooy` contains the python file to connect to the mongodb client and insert records
2. `mongodb.yaml` contains the config file (containing mongo login), mongo deployment, and service
3. `mongo-python.yaml` contains the deployment for the pod with python container which interacts with the mongo database pod 
4. `Dockerfile` is used to build the image which is then deployed using `mongo-python.yaml`
   1. Gets requirements from `requirements.txt`

## Running the files

### Overview
The first step in deploying the kubernetes mongo database and python client is to create
a docker image which can be deployed to the kubernetes cluster.

The final step is to deploy the `mongodb.yaml` and `mongo-python.yaml` files in the cluster.

The files are automatically set to insert records, and we can see that from the logs.

### Creating Docker Image
If you would like to create a new docker image for this mongo python deployment, follow these steps, 
otherwise, my docker image should still be able to be deployed with the current configuration.

In the folder where the `Dockerfile` is, run the following
```angular2html
docker build . -t [DOCKER ACCOUNT]/pymongo-kb
```

You can then push the file to your docker repository
```angular2html
docker login
docker push [DOCKER ACCOUNT]/pymongo-kb
```

If you decide to do this, you need to edit the image in the deployment file. On line 24 of 
`mongo-python.yaml`, change the image to the following:

```angular2html
image: [DOCKER ACCOUNT]/pymongo-kb
```

### Pod and Service Deployment
In a terminal create a kubernetes cluster, cd into this repo and deploy the `mongodb.yaml` and `mongo-python.yaml` files.

```angular2html
minikube start
kubectl apply -f mongodb.yaml
kubectl apply -f mongo-python.yaml
```

### Checking File Logs
You can see if the connection to the mongodb from python client was successful using the following:
```angular2html
kubectl logs -f deployment.apps/mongo-python
```

