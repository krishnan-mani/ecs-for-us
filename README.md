Outline
===

- Create a container for a (simple) API
- Create an ECS cluster
- Deploy the API to ECS
- Configure a load balancer, send traffic to the API
- Scale the API up
- Make a change, and deploy a new version

Pre-requisites
===

- build and run Docker images locally
- personal account on dockerhub.io
- AWS credentials and privileges
- Software installed
    - `git`
    - `curl`
    - `docker`
    - `docker-for-windows`
    - `virtualenv`

Workshop
===

- Run API locally

```
$ virtualenv venv
$ source venv/bin/activate # or `source venv/Scripts/activate` on Windows
$ pip install -r requirements.txt
$ python ./example.py
$ curl localhost:5000/example/

```

- Create Docker image and run container locally

```
$ docker ps
$ docker build . -t my-service:1
$ docker images
$ docker run -d -p 5000:5000 my-service:1
$ curl 192.168.99.100:5000/example/

```

- Push the image to dockerhub registry

```
$ docker tag my-service:1 kmdemos/my-service:1
$ docker login
$ docker push kmdemos/my-service:1

```

- Create and register a task definition for the API

```
$ export AWS_REGION=eu-west-1
$ export AWS_PROFILE=nonprod
$ aws configure list
$ aws sts get-caller-identity
$ aws --region eu-west-1 ecs register-task-definition \
    --cli-input-json file://task_definition.json

```

- Deploy the ECS cluster

```
$ aws cloudformation create-stack \
    --stack-name ecs-workshop-manik \
    --template-body file://template.json \
    --parameters file://parameters.json \
    --capabilities CAPABILITY_IAM

```

- TODO: Deploy our API to the cluster