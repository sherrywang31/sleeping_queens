# Makefile
SHELL = /bin/bash

# Env
.PHONY: env
env:
	python3.12 -m venv venv  # recommend using Python 3.10
	source venv/bin/activate  # on Windows: venv\Scripts\activate
	#python3.12 -m pip install --upgrade pip setuptools wheel
	python3.12 -m pip install -r requirements.txt

# Cleaning
.PHONY: clean
clean: style
	python notebooks/clear_cell_nums.py
	find . -type f -name "*.DS_Store" -ls -delete
	find . | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf
	find . | grep -E ".pytest_cache" | xargs rm -rf
	find . | grep -E ".ipynb_checkpoints" | xargs rm -rf
	rm -rf .coverage*

# Styling
.PHONY: style
style:
	black .
	flake8
	python3 -m isort .
	pyupgrade

