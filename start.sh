#!/bin/bash

docker stop $(docker ps -aq)
kubectl delete deployment --all
kubectl delete service --all
kubectl delete pods --all
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker rmi $(docker images -q)

docker build -t ziffer99/workflow-opener:2.0 -f ./workflow_opener_2/Dockerfile --no-cache
docker push ziffer99/workflow-opener:2.0

docker build -t ziffer99/faas:3.0 -f ./faas/Dockerfile --no-cache
docker push ziffer99/faas:3.0

kubectl apply -f aggregated.yml
docker rm $(docker ps -aq)
docker rmi $(docker images -q)
kubectl expose service minio1 --type=NodePort --target-port=9001 --name=minio1-np
kubectl expose service rabbitmq --type=NodePort --target-port=15672 --name=rabbitmq-np
kubectl get svc
kubectl get pods