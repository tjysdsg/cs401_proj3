set -e
set -u
set -o pipefail

# delete existing ones
kubectl delete --ignore-not-found=true configmap pyfile
kubectl delete --ignore-not-found=true configmap outputkey

kubectl create configmap pyfile --from-file pyfile=module.py --output yaml
kubectl create configmap outputkey --from-literal REDIS_OUTPUT_KEY=jt304-proj3-output --output yaml
