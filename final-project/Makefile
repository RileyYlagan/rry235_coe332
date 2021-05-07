NSPACE="rileyylagan"
NSPACE2="rry235final"
APP="rry235final-app"
VER="0.1.0"
RPORT="6419"
FPORT="5039"
UID="869725"
GID="816966"

build-db:
	docker build -t ${NSPACE}/${APP}-db:${VER} \
                     -f docker/Dockerfile.db \
                     ./

build-api:
	docker build -t ${NSPACE}/${APP}-api:${VER} \
                     -f docker/Dockerfile.api \
                     ./

build-wrk:
	docker build -t ${NSPACE}/${APP}-wrk:${VER} \
                     -f docker/Dockerfile.wrk \
                     ./

test-db: build-db
	docker run --name ${NSPACE2}-db \
                   --network ${NSPACE2}-network-test \
                   -p ${RPORT}:6379 \
                   -d \
                   -u ${UID}:${GID} \
                   -v ${PWD}/data/:/data \
                   ${NSPACE}/${APP}-db:${VER}

test-api: build-api
	docker run --name ${NSPACE2}-api \
                   --network ${NSPACE2}-network-test \
                   --env REDIS_IP=${NSPACE2}-db \
                   -p ${FPORT}:5000 \
                   -d \
                   ${NSPACE}/${APP}-api:${VER} 

test-wrk: build-wrk
	docker run --name ${NSPACE2}-wrk \
                   --network ${NSPACE2}-network-test \
                   --env REDIS_IP=${NSPACE2}-db \
                   -d \
                   ${NSPACE}/${APP}-wrk:${VER} 

clean-db:
	docker ps -a | grep ${NSPACE2}-db | awk '{print $$1}' | xargs docker rm -f

clean-api:
	docker ps -a | grep ${NSPACE2}-api | awk '{print $$1}' | xargs docker rm -f

clean-wrk:
	docker ps -a | grep ${NSPACE2}-wrk | awk '{print $$1}' | xargs docker rm -f

	
build-all: build-db build-api build-wrk

test-all: test-db test-api test-wrk

clean-all: clean-db clean-api clean-wrk

push-all: 
	VER=${VER} docker push ${NSPACE}/${APP}-api:${VER}
	VER=${VER} docker push ${NSPACE}/${APP}-db:${VER}
	VER=${VER} docker push ${NSPACE}/${APP}-wrk:${VER}

compose-up:
	VER=${VER} docker-compose -f docker/docker-compose.yml pull
	VER=${VER} docker-compose -f docker/docker-compose.yml -p ${NSPACE} up -d --build ${NSPACE2}-db
	VER=${VER} docker-compose -f docker/docker-compose.yml -p ${NSPACE} up -d --build ${NSPACE2}-api
	sleep 5
	VER=${VER} docker-compose -f docker/docker-compose.yml -p ${NSPACE} up -d --build ${NSPACE2}-wrk

compose-down:
	VER=${VER} docker-compose -f docker/docker-compose.yml -p ${NSPACE} down

restart: compose-down build-all push-all compose-up
	docker ps -a | grep rileyylagan



k-test:
	cat kubernetes/test/* | TAG=${VER} envsubst '$${TAG}' | yq | kubectl apply -f -

k-test-del:
	cat kubernetes/test/*deployment.yml | TAG=${VER} envsubst '$${TAG}' | yq | kubectl delete -f -


k-prod:
	cat kubernetes/prod/* | TAG=${VER} envsubst '$${TAG}' | yq | kubectl apply -f -

k-prod-del:
	cat kubernetes/prod/*deployment.yml | TAG=${VER} envsubst '$${TAG}' | yq | kubectl delete -f -