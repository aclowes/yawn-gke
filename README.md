# YAWN on GKE

[![Docker Repository on Quay](https://quay.io/repository/aclowes/yawn-gke/status 
"Docker Repository on Quay")](https://quay.io/repository/aclowes/yawn-gke)

This tutorial is describes setting up a [Google Container Engine
](https://cloud.google.com/container-engine/) (GKE) cluster running 
[YAWN](github.com/aclowes/yawn), a workflow engine written in Python.

### Setting up a Kubernetes cluster on Google Cloud

The [GKE tutorial](https://cloud.google.com/container-engine/docs/quickstart) 
is a great place to start. Once you have installed the `gcloud` SDK, you 
can follow these steps.

    # setup kubectl and create a cluster
    gcloud components install kubectl
    gcloud config set compute/zone us-central1-b
    gcloud container clusters create yawn
    
    # create a persistent SSD disk for postgres
    gcloud compute disks create --size=10GB --type=pd-ssd postgres-data
    
    # create the yawn resources
    kubectl create -f postgres-db-deployment.yaml
    kubectl create -f postgres-db-service.yaml
    kubectl create -f yawn-webserver-deployment.yaml
    kubectl create -f yawn-webserver-service.yaml
    kubectl create -f yawn-worker-deployment.yaml
    
    # actions on services, pods, secrets, etc
    kubectl get service
    kubectl get service yawn-webserver -o yaml  # show as yaml
    kubectl describe pod postgres-db
    kubectl replace -f yawn-webserver-deployment.yaml
    kubectl scale deployment yawn-webserver --replicas=2 
    
    # run the migrations
    kubectl get pods 
    kubectl exec <pod name> -- yawn migrate
    
    # view container logs
    kubectl logs yawn-webserver-421291050-jz04j
    
    # ssh into a node
    kubectl get nodes
    gcloud compute ssh <node>

To easily get a free SSL certificate:

    # Register your domain at:
    https://domains.google.com/registrar
    
    # Once registered, add an 'A' record pointing to the IP address
    # created by your ingress in the section 'Custom resource records'
    https://domains.google.com/registrar

    # Name              Type   Data
    # _acme-challenge   TXT    <token from certbot>
    
    # Install the Let’s Encrypt agent 'certbot' and request a cert
    brew install certbot
    sudo certbot certonly --manual --preferred-challenges dns -d yawn.live
    
Another good resource is the [kubectl cheatsheet](
https://kubernetes.io/docs/user-guide/kubectl-cheatsheet/).
