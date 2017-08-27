Common Kubernetes commands

    # actions on services, pods, secrets, etc
    kubectl get service
    kubectl describe pod postgres-db
    
    kubectl create -f yawn-webserver-deployment.yaml
    kubectl replace -f yawn-webserver-deployment.yaml
    
    kubectl scale deployment yawn-webserver --replicas=2 

https://kubernetes.io/docs/user-guide/kubectl-cheatsheet/