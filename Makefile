.PHONY: deploy check-env
COMPOSE=docker-compose
SERVICE=docker_monitor

deploy: check-env deps
	$(COMPOSE) up --build -d $(SERVICE)

logs: check-env
	$(COMPOSE) logs --tail 500 -f $(SERVICE)

stop: check-env
	$(COMPOSE) stop $(SERVICE)

check-env:
ifndef ENV
	$(error ENV is undefined)
endif

deps:
	pipenv lock -r > requirements.txt
