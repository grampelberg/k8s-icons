.PHONY: build
build:
	docker build -t iconbuilder:latest -f Dockerfile .

	docker run iconbuilder:latest > k8s.svg

