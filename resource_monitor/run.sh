set -e
set -u
set -o pipefail

./generate_config_maps.sh
kubectl delete --ignore-not-found=true deploy serverless-redis # delete existing one
kubectl apply -f serverless-deployment.yaml
kubectl get deployments
