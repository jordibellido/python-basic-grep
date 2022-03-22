all: test

test:
	python3 -m pytest grep_test.py
.PHONY: test

clean:
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
	rm --recursive --force */.pytest_cache/ .pytest_cache/
