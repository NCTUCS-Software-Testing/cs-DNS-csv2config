run:
	python3 cover_host.py
test:
	coverage3 run test_cover_host.py
	coverage3 report -m
