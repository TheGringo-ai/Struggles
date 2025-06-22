# === Project Makefile ===

bootstrap:
	./tools/bootstrap.sh

run:
	./tools/run_dev.sh

env:
	python3 tools/generate_env.py

clean:
	rm -rf .venv .python-version __pycache__

help:
	@echo "make bootstrap   # Set up environment"
	@echo "make run         # Run development app"
	@echo "make env         # Generate .env file"
	@echo "make clean       # Remove environment & cache"
