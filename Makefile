.PHONY: req
req:
	pip3 install -r requirements.txt

.PHONY: start
start:
	python3 main.py	