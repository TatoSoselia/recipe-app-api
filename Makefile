# Makefile to manage Docker and Django operations

# Help command to display all available commands with descriptions
help:
	@echo "Available commands:"
	@echo "  startapp         - Create a new Django app. Usage: 'make startapp <APP_AME>'"
	@echo "  makemigrations   - Create migration files for Django models. Usage: 'make makemigrations'"
	@echo "  migrate          - Apply database migrations. Usage: 'make migrate'"
	@echo "  lint             - Run flake8 to lint the code. Usage: 'make lint'"
	@echo "  test             - Run test. Usage: 'make test'"

# If the first argument is "startapp", then use the rest as arguments for "startapp"
ifeq (startapp,$(firstword $(MAKECMDGOALS)))
  # Use the rest as arguments for "startapp"
  STARTAPP_ARGS := $(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS))
  # Turn them into do-nothing targets
  $(eval $(STARTAPP_ARGS):;@:)
endif

# Create a new Django app
startapp:
	@echo "Creating a new Django app named $(STARTAPP_ARGS)..."
	docker-compose run --rm api sh -c "cd modules && mkdir $(STARTAPP_ARGS) && \
	django-admin startapp $(STARTAPP_ARGS) $(STARTAPP_ARGS) && \
	cd $(STARTAPP_ARGS) && rm tests.py && \
	mkdir tests && cd tests && touch __init__.py"


# Create migration files
makemigrations:
	@echo "Making migration files..."
	docker compose run --rm api python manage.py makemigrations

# Run migrations
migrate:
	@echo "Running migrations in Docker..."
	docker compose run --rm api python manage.py migrate

# Lint the code with flake8
lint:
	@echo "Running flake8 for code linting..."
	docker compose run --rm api flake8

# Test the code
test:
	@echo "Running Tests..."
	docker compose run --rm api python manage.py test