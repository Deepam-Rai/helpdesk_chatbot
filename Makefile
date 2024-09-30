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

start-action:
	docker compose up action-server -d

start-duckling:
	docker compose up duckling -d

train-redeploy-logs:
	make -f Makefile train
	make -f Makefile stop
	make -f Makefile run
	make -f Makefile core-logs

redeploy-logs:
	make -f Makefile stop
	make -f Makefile run
	make -f Makefile core-logs

action-redeploy-logs:
	make restart-action
	make action-logs

ngrok:
	ngrok http 5006
	#ngrok http 5006 --domain=your-static-domain.ngrok-free.app

build:
	docker compose build


ui:
	echo "http://localhost:7999/"
	python -m http.server 7999

visualize:
	rasa visualize --domain domain
