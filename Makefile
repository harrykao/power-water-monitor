.PHONY: \
	black \
	black_check \
	build \
	dev_image \
	flake8 \
	integration_test \
	isort \
	isort_check \
	mypy \
	run \
	shell

ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))


build:
	docker build -t energy_water_monitor .

run: build
	docker run -it --rm --env-file=env --init energy_water_monitor

shell: build
	docker run -it --rm --env-file=env \
		--volume $(ROOT_DIR)/src:/src \
		--volume $(ROOT_DIR)/work:/work \
		--entrypoint /bin/sh energy_water_monitor


dev_image: .last_build_flag_dev

.last_build_flag_dev: Dockerfile.dev
	docker build -f Dockerfile.dev -t energy_water_monitor_tools .
	@touch .last_build_flag_dev

RUN_DEV_TOOL = docker run --rm -t --volume $(ROOT_DIR)/src:/src -w /src energy_water_monitor_tools

black: dev_image
	@$(RUN_DEV_TOOL) black .

black_check: dev_image
	@$(RUN_DEV_TOOL) black --check .

flake8: dev_image
	@$(RUN_DEV_TOOL) flake8

isort: dev_image
	@$(RUN_DEV_TOOL) isort .

isort_check: dev_image
	@$(RUN_DEV_TOOL) isort --check-only .

mypy: dev_image
	@$(RUN_DEV_TOOL) mypy .
