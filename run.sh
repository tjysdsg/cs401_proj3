kubectl apply -f serverless-deployment.yaml || exit 1
kubectl get deployments || exit 1
kubectl get services
