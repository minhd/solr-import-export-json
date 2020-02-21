init:
	python3 -m venv venv
	make install

clean-pyc:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete

clean:	clean-pyc

install:
	venv/bin/pip install -r requirements.txt

test:	clean-pyc
	venv/bin/python -m unittest discover -s tests -p "*_test.py"