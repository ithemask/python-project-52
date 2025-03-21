install:
	uv sync
makemigrations:
	uv run python manage.py makemigrations
migrate:
	uv run python manage.py migrate
makemessages:
	uv run django-admin makemessages -l ru
compilemessages:
	uv run django-admin compilemessages
start-dev:
	uv run python manage.py runserver
start-prod:
	uv run python -m gunicorn task_manager.asgi:application -k uvicorn.workers.UvicornWorker
lint:
	uv run ruff check
test:
	uv run python manage.py test
