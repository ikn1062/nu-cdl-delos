# Helm Chart

## Important Files
1. `app/` contains the fast api python file that contains the  route “/initiate”
2. `myfastapi/` contains all the deployment, service, and ingress files integrated as a helm chart. This also includes prometheus as a subchart.
3. `Dockerfile` is used to build the image which is then deployed using the helm chart
   1. Gets requirements from `requirements.txt`
4. `api-deployment.yaml` holds the deployment, service, and ingress used during debugging

## Running the files

### Overview
The first step in deploying the kubernetes application microservice using helm is to create
a docker image which can be deployed to the kubernetes cluster.

The next step is to create the kubernetes cluster and deploy the pod, service, and ingress 
using helm. Finally, you can ping “http://<your-ingress-host-name>/initiate from your browser.

### Creating Docker Image
If you would like to create a new docker image for this helm chart, follow these steps, 
otherwise, my docker image should still be able to be deployed using the current helm chart.

In the folder where the `Dockerfile` is, run the following
```angular2html
docker build . -t [DOCKER ACCOUNT]/fastapi-k8s
```

You can then push the file to your docker repository
```angular2html
docker login
docker push [DOCKER ACCOUNT]/fastapi-k8s
```

If you decide to do this, you need to edit the image in the helm chart. On line 8 of 
`myfastapi/values.yaml`, change the repository to the following:

```angular2html
image:
  repository: [DOCKER ACCOUNT]/fastapi-k8s
```

### Installing Helm Chart
In a terminal create a kubernetes cluster, cd into this repo and then install the helm chart.

```angular2html
minikube start
helm install [FASTAPI DEPLOYMENT NAME] ./myfastapi
```

### Pinging Microservice
If you're using docker to hold the kubernetes cluster, use before trying to ping microservice.
```angular2html
minikube tunnel
```

You can then go to a browser and open http://myapp.kube/initiate to get
`Microservice is successfully triggered`

If this does not work, might need to add myapp.kube to `/etc/hosts`. To do this, cd to
your home directory, and then type `vi /etc/hosts` to add `127.0.0.1 myapp.kube` to the file.

