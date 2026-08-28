.PHONY: help setup run-backend run-frontend test-backend test-frontend build docker-up docker-down

help:
	@echo "Nexus Tech Store Developer Tasks"
	@echo "--------------------------------"
	@echo "make setup          : Install backend and frontend dependencies"
	@echo "make run-backend    : Launch Django development server"
	@echo "make run-frontend   : Launch React Vite development server"
	@echo "make test           : Run backend test suite"
	@echo "make build          : Build production frontend bundle"
	@echo "make docker-up      : Spin up Docker Compose cluster"
	@echo "make docker-down    : Stop Docker Compose containers"

setup:
	pip install -r backend/requirements.txt
	cd frontend && npm install

run-backend:
	cd backend && python manage.py runserver

run-frontend:
	cd frontend && npm run dev

test:
	cd backend && python manage.py test store

build:
	cd frontend && npm run build

docker-up:
	docker-compose up -d --build

docker-down:
	docker-compose down
