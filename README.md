# Food-Order-Service Development
The development environment can be started using Docker and Docker compose
tools. The docker-compose will create a container named `backend-api`

### Environment and setup
Set up the following environment variables:
export BASE_API_URL="https://nourish.me/api"
export CLIENT_API_KEY="CLIENT_API_KEY"
export ENVIRONMENT=(prod or stage) default is "dev"

#### Build image

The first time you start the environment you will need some extra steps. First
of them is creating the docker image.
```
$ cd food_order_system
$ docker-compose build
```

#### How it works
The main
