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
- `virtualenv`
- `git`
- AWS credentials and privileges

Workshop
===

- Run API locally

```
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python ./example.py
$ curl http://localhost:5000/example/

```

- Create and run Docker container for API

```
$ docker ps
$ docker build . -t my-service:1
$ docker images
$ docker run -d -p 5000:5000 my-service:1
$ curl 192.168.99.100:5000/example/

```
