Outline
===

- Create a container for a (simple) API
- Create an ECS cluster with application load balancer
- Deploy the API to ECS
- Make a change, and deploy a new version

Pre-requisites
===

- build and run Docker images locally. You may choose to use `docker-machine`, OR alternatively, native support for Dockers in Windows or Linux
- personal account on [Docker Hub](https://hub.docker.com/)
- AWS credentials for a privileged user 
- Software installed
    - `git`
    - `curl`
    - `docker`
    - `docker-for-windows` (optional)
    - `virtualenv`

Workshop
===

_Note_: Certain instructions below assume the use of `docker-machine`. Ignore them if they are not applicable to you.

- Run API locally

```bash
$ virtualenv venv
$ source venv/bin/activate # or `source venv/Scripts/activate` on Windows
$ pip install -r requirements.txt
$ python ./example.py
$ curl --silent localhost:5000/example/
# Expect a response from the API running locally

```

- Create Docker image and run container locally

```bash
# obtain the docker-machine name
$ docker-machine ls 
$ eval $(docker-machine env [DOCKER_MACHINE_NAME])

$ docker build . -t my-service:1
$ docker images
$ docker run -d -p 5000:5000 my-service:1
$ docker ps
$ docker-machine ip [DOCKER_MACHINE_NAME]
$ curl --silent [DOCKER_MACHINE_IP]:5000/example/
# Expect a response from the API running as a container

```

- Push the image to a registry on Docker Hub

```bash
# [USERNAME] is your username on Docker Hub 
$ docker tag my-service:1 [USERNAME]/my-service:1
$ docker login
$ docker push [USERNAME]/my-service:1

```

- Deploy the ECS cluster

```bash
$ export AWS_REGION=eu-west-1
$ export AWS_PROFILE=nonprod
$ aws configure list
$ aws sts get-caller-identity

$ cp starter-parameters.example.json starter-parameters.json
# Edit starter-parameters.json and supply the required information (from the `dev` environment)

# Choose a name for the CloudFormation stack you will provision, say [`ecs-workshop-USERNAME`]
$ aws cloudformation create-stack \
    --stack-name [ecs-workshop-USERNAME] \
    --template-body file://starter-template.json \
    --parameters file://starter-parameters.json \
    --capabilities CAPABILITY_IAM

$ aws cloudformation describe-stacks \
    --stack-name [ecs-workshop-USERNAME] \
    --query "Stacks[0].Outputs"
$ curl --silent [LOAD_BALANCER_DNS]

```

- Deploy our API to the cluster

```bash
$ cp starter-template.json template.json 
# Edit this template.json file for all subsequent changes
# Add the following for the API:
    - task definition
    - service
    - target group
    - listener rule

# Add the information needed for stack parameters
$ cp starter-parameters.json parameters.json

# Update the CloudFormation stack    
$ aws cloudformation update-stack \
    --stack-name [ecs-workshop-USERNAME] \
    --template-body file://template.json \
    --parameters file://parameters.json \
    --capabilities CAPABILITY_IAM
$ aws cloudformation describe-stack-events \
    --stack-name [ecs-workshop-USERNAME]
$ curl --silent [LOAD_BALANCER_DNS]/example/

```

- Modify service (bump `DesiredCount`) and witness scaling activity

```bash
$ aws ecs update-service \
    --service-arn [SERVICE_ARN] \
    --cluster [CLUSTER_NAME]
    --desired-count 3

```

- Deploy new version of the API

```bash
# Change application code, build new Docker image version, and push
$ docker build . -t my-service:2 -t [USERNAME]/my-service:2
$ docker push [USERNAME]/my-service:2 

# update the template and the parameters, then update the stack
$ aws cloudformation update-stack \
    --stack-name [ecs-workshop-USERNAME] \
    --template-body file://template.json \
    --parameters file://parameters.json \
    --capabilities CAPABILITY_IAM  

```

- Remember to delete your stack!

```
$ aws cloudformation delete-stack --stack-name [ecs-workshop-USERNAME]
$ aws cloudformation describe-stacks --stack-name [ecs-workshop-USERNAME]

```
