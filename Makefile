.PHONY: build run test dev lint clean help

# Default target
help:
	@echo "Network Discovery Tool Docker Makefile"
	@echo "======================================"
	@echo ""
	@echo "Available targets:"
	@echo "  build      - Build the Docker image"
	@echo "  run        - Run the network discovery tool (use ARGS='192.168.1.0/24' to pass arguments)"
	@echo "  test       - Run tests (use ARGS='tests/test_scanner.py' to specify tests)"
	@echo "  dev        - Start a development shell"
	@echo "  lint       - Run linters (flake8, black, isort, mypy)"
	@echo "  clean      - Remove Docker containers, images, and build artifacts"
	@echo "  help       - Show this help message"
	@echo ""
	@echo "Examples:"
	@echo "  make run ARGS='192.168.1.0/24 -f csv'"
	@echo "  make test ARGS='tests/test_scanner.py -v'"
	@echo ""

# Build the Docker image
build:
	docker-compose build

# Run the network discovery tool
run: build
	docker-compose run --rm network-discovery $(ARGS)

# Run tests
test: build
	docker-compose run --rm test $(ARGS)

# Start a development shell
dev: build
	docker-compose run --rm dev

# Run linters
lint: build
	docker-compose run --rm dev bash -c "flake8 src tests && black src tests && isort src tests && mypy src tests"

# Clean up
clean:
	docker-compose down --rmi local
	rm -rf output/*.html output/*.csv output/*.xlsx output/*.json
	rm -rf devices.json
	rm -rf __pycache__ .pytest_cache
	find . -name "*.pyc" -delete
