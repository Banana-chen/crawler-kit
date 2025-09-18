export UV_PROJECT_ENVIRONMENT=src/venv
export IMAGE_REPOSITORY=asia-east1-docker.pkg.dev/crawler-kit/crawler-kit/test

.PHONY: \
	dev \
	format \
	lint \
	test \
	deploy \
	install \
	install-full \
	tree \
	freeze \
	build \
	push \
	clean

format:
	@uvx ruff format .

dev:
	@firebase emulators:start --only functions,pubsub

lint:
	@uvx ruff check .

test:
	@uv run pytest

deploy:
	@firebase deploy --only functions

install:
	@uv pip install -e ".[cloud,cli,dev]"

install-full:
	@uv pip install -e ".[cloud,workflow,web,browser,cli,dev]"

tree:
	@tree -I 'build|__pycache__|*.egg-info|venv|.venv|*.log|downloaded_files|CapSolver.Browser.Extension-v1.16'

freeze:
	@uv pip compile pyproject.toml --extra cloud > src/requirements.txt

clean:
	@rm -rf build/ dist/ *.egg-info/ __pycache__/ .pytest_cache/
	@find . -name "*.pyc" -delete

push:
	@docker push $(IMAGE_REPOSITORY):latest

build:
	@docker build --platform=linux/amd64 . -t $(IMAGE_REPOSITORY):latest