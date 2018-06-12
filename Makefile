run:
	python3 cover_host.py
test:
	coverage run test_cover_host.py
	coverage report -m
clean:
	find ./working/* -not -name "*.md" -delete
