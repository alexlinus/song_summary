

# shortcuts
up:
	docker compose -f local.yml up -d

stop:
	docker compose -f local.yml stop


install:
	poetry install

test:
	pytest .