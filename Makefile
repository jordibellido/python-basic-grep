all: test

test: test_grep test_search
	python3 -m pytest grep_test.py
	python3 -m pytest grep_search.py
.PHONY: test

test_grep:
	python3 -m pytest grep_test.py
.PHONY: test_grep

test_search:
	python3 -m pytest search_test.py -s
.PHONY: test_search

clean:
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
	rm --recursive --force */.pytest_cache/ .pytest_cache/
