# YAWN on GKE

[![Docker Repository on Quay](https://quay.io/repository/aclowes/yawn-gke/status 
"Docker Repository on Quay")](https://quay.io/repository/aclowes/yawn-gke)

This tutorial is describes setting up a [Google Container Engine
](https://cloud.google.com/container-engine/) (GKE) cluster running 
[YAWN](https://github.com/aclowes/yawn), a workflow engine written in Python.

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
  
    # create a secrets file and fill in the secrets
    cp secrets-template.yaml secrets.yaml
    kubectl create -f secrets.yaml
    
    # create the yawn resources
    kubectl create -f postgres-db-deployment.yaml
    kubectl create -f postgres-db-service.yaml
    kubectl create -f yawn-webserver-deployment.yaml
    kubectl create -f yawn-webserver-service.yaml
    kubectl create -f yawn-worker-deployment.yaml
    
    # run the migrations - pick any pod to run them on
    kubectl get pods 
    kubectl exec <pod name> -- yawn migrate

There are a few manual steps to get the load balancer health check working. 
Go to the [Health Checks] and select the health check with path '/' (the other
check is for the kubernetes admin website). Edit it, and change the path to 
'/api/healthy/' and the host to your domain name, here 'yawn.live'. The health
check endpoint is exempt from SSL redirection, but it must have a host header in
Django's ALLOWED_HOSTS setting.

[Health Checks]: https://console.cloud.google.com/compute/healthChecks?project=wise-vim-178017
    
    # actions on services, pods, secrets, etc
    kubectl get service
    kubectl get service yawn-webserver -o yaml  # show as yaml
    kubectl describe pod postgres-db
    kubectl replace -f yawn-webserver-deployment.yaml
    kubectl scale deployment yawn-webserver --replicas=2 
        
    # view container logs
    kubectl logs yawn-webserver-421291050-jz04j
    
    # ssh into a node
    kubectl get nodes
    gcloud compute ssh <node>
    
    # exec in a running pod
    kubectl exec -it <pod name> bash
    
    # access the admin GUI at http://127.0.0.1:8001/ui/
    kubectl proxy

To easily get a free SSL certificate:

    # Register your domain at:
    https://domains.google.com/registrar
    
    # Once registered, add an 'A' record pointing to the IP address
    # created by your ingress in the section 'Custom resource records'

    # Install the Let’s Encrypt agent 'certbot' and request a cert
    brew install certbot
    sudo certbot certonly --manual --preferred-challenges dns -d yawn.live

    # Make a TXT DNS record as directed by the tool, and wait a few minutes to propogate
    # Name              Type   Data
    # _acme-challenge   TXT    <token from certbot>

    # Update the secrets.yaml file with the new base64 encoded chain and key
    sudo base64 /etc/letsencrypt/live/yawn.live/fullchain.pem | pbcopy
    sudo base64 /etc/letsencrypt/live/yawn.live/privkey.pem | pbcopy

    # Then restart the ingress
    kubectl replace --force -f secrets.yaml
    kubectl replace --force -f yawn-ingress.yaml

    # Check that the new certificate is being used after a few inutes:
    curl -v https://yawn.live 2>&1 | grep expire
    
    # If the yawn-webserver pods are showing as unhealthy, fix the 
    # healthcheck per the above instructions.
    
Another good resource is the [kubectl cheatsheet](
https://kubernetes.io/docs/user-guide/kubectl-cheatsheet/).

This site serves static files created by the tasks directly from google cloud
storage.

    gsutil mb gs://static.yawn.live
    gsutil web set -m index.html -e 404.html gs://static.yawn.live
