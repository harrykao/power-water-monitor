build:
	docker build -t energy_water_monitor .

run: build
	docker run -it --rm --env-file=env energy_water_monitor

shell: build
	docker run -it --rm --env-file=env --entrypoint /bin/sh energy_water_monitor
