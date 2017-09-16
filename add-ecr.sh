#!/bin/bash
REPO_NAME=$1
BUILD_DIR=$2
ACC_NUM=$3
if [ $# -ne 3 ]; then
    echo $0: usage: $0 REPO_NAME BUILD_DIR ACC_NUM
    exit 1
fi
$(aws ecr get-login  --no-include-email --region us-east-1)
docker build -t $REPO_NAME $BUILD_DIR 
docker tag $REPO_NAME:latest $ACC_NUM.dkr.ecr.us-east-1.amazonaws.com/$REPO_NAME:latest
docker push $ACC_NUM.dkr.ecr.us-east-1.amazonaws.com/$REPO_NAME:latest
