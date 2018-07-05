Outline
===

- Create a container for a (simple) API
- Create an ECS cluster with application load balancer
- Deploy the API to ECS
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

```bash
$ virtualenv venv
$ source venv/bin/activate # or `source venv/Scripts/activate` on Windows
$ pip install -r requirements.txt
$ python ./example.py
$ curl --silent localhost:5000/example/

```

- Create Docker image and run container locally

```bash
$ docker ps
$ docker build . -t my-service:1
$ docker images
$ docker run -d -p 5000:5000 my-service:1
$ curl --silent 192.168.99.100:5000/example/

```

- Push the image to dockerhub registry

```bash
$ docker tag my-service:1 kmdemos/my-service:1
$ docker login
$ docker push kmdemos/my-service:1

```

- Create and register a task definition for the API

```bash
$ export AWS_REGION=eu-west-1
$ export AWS_PROFILE=nonprod
$ aws configure list
$ aws sts get-caller-identity
$ aws --region eu-west-1 ecs register-task-definition \
    --cli-input-json file://task_definition.json

```

- Deploy the ECS cluster

```bash
$ aws cloudformation create-stack \
    --stack-name ecs-workshop-manik \
    --template-body file://template.json \
    --parameters file://parameters.json \
    --capabilities CAPABILITY_IAM

$ aws cloudformation describe-stacks \
    --stack-name ecs-workshop-manik \
    --query "Stacks[0].Outputs"
$ curl --silent [LOAD_BALANCER_DNS]

```

- Deploy our API to the cluster

```bash
$ aws cloudformation update-stack \
    --stack-name ecs-workshop-manik \
    --template-body file://template.json \
    --parameters file://parameters.json \
    --capabilities CAPABILITY_IAM
$ curl --silent [LOAD_BALANCER_DNS]/example/    

```

- Modify service (bump `DesiredCount`)

```bash
$ aws ecs update-service \
    --service-arn [SERVICE_ARN] \
    --cluster [CLUSTER_NAME]
    --desired-count 1

```

- Deploy new version of the API

```bash
# Change application code, build new Docker image version, and push
$ docker build . -t my-service:2
$ docker images
$ docker tag [IMAGE_ID] kmdemos/my-service:2
$ docker push kmdemos/my-service:2 

# Update task definition
# Update service

```