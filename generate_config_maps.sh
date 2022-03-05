# should only run once
kubectl create configmap pyfile --from-file pyfile=resource_monitor/module.py --output yaml
kubectl create configmap outputkey --from-literal REDIS_OUTPUT_KEY=jt304-proj3-output --output yaml
