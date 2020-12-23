.PHONY: build run exec
WINDOW_SIZE := 1024,768
# Here Basic URL
BASE_URL :=
# Here Compare URL
COMPARE_URL :=

build:
	docker-compose build

run:build
	WINDOW_SIZE=1024,768 \
	BASE_URL=$(BASE_URL) \
	COMPARE_URL=$(COMPARE_URL) \
	ENABLE_SHOW_DIFF=$(ENABLE_SHOW_DIFF) \
	docker-compose run --rm app

exec:
	docker-compose run --rm app bash