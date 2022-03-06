docker build . --no-cache -t quay.io/tjysdsg/serverless_runtime:latest || exit 1
docker push quay.io/tjysdsg/serverless_runtime:latest