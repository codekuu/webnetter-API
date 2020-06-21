.PHONY: init
install:
	pip install -r requirements.txt

.PHONY: start_dev_env
start_dev_env:
	python backend/app.py

