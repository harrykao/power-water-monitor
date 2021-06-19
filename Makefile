build:
	docker build -t energy_water_monitor .

run: build
	docker run -it --rm energy_water_monitor

shell: build
	docker run -it --rm --entrypoint /bin/sh energy_water_monitor
