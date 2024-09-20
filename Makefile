train:
	docker compose run --rm core-server rasa train --domain domain --config config.yml --fixed-model-name helpdesk_model --debug

run:
	docker compose up -d

stop:
	docker compose down

core-logs:
	docker compose logs -f core-server

action-logs:
	docker compose logs -f action-server

restart-core:
	docker compose restart core-server

restart-action:
	docker compose restart action-server

train-redeploy-logs:
	make -f Makefile train
	make -f Makefile stop
	make -f Makefile run
	make -f Makefile core-logs

redeploy-logs:
	make -f Makefile stop
	make -f Makefile run
	make -f Makefile core-logs

build:
	docker compose build


ui:
	python -m http.server 7999
