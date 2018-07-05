Outline
===

- Create a container for a (simple) API
- Create an ECS cluster with application load balancer
- Deploy the API to ECS
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
$ docker-machine ls # obtain the docker-machine name
$ docker-machine ip [DOCKER_MACHINE_NAME]
$ curl --silent [DOCKER_MACHINE_IP]:5000/example/

```

- Push the image to dockerhub registry

```bash
$ docker tag my-service:1 kmdemos/my-service:1
$ docker login
$ docker push [DOCKERHUB_USERNAME]/my-service:1

```

- Create and register a task definition for the API

```bash
$ export AWS_REGION=eu-west-1
$ export AWS_PROFILE=nonprod
$ aws configure list
$ aws sts get-caller-identity

```

- Deploy the ECS cluster

```bash
$ cp starter-parameters.json parameters.json
# Edit parameters.json and supply the required information (from the `dev` environment)

$ aws cloudformation create-stack \
    --stack-name ecs-workshop-manik \
    --template-body file://starter-template.json \
    --parameters file://parameters.json \
    --capabilities CAPABILITY_IAM

$ aws cloudformation describe-stacks \
    --stack-name ecs-workshop-manik \
    --query "Stacks[0].Outputs"
$ curl --silent [LOAD_BALANCER_DNS]

```

- Deploy our API to the cluster

```bash
$ cp starter-template.json template.json 
# Edit this template.json file for all subsequent changes

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
    --desired-count 3

```

- Deploy new version of the API

```bash
# Change application code, build new Docker image version, and push
$ docker build . -t my-service:2 -t kmdemos/my-service:2
$ docker push kmdemos/my-service:2 

# update the template and the parameters, then update the stack
$ aws cloudformation update-stack \
    --stack-name ecs-workshop-manik \
    --template-body file://template.json \
    --parameters file://parameters.json \
    --capabilities CAPABILITY_IAM  

```