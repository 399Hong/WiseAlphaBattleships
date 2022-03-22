default:
	python3 main.py
clean:
	rm -rf __pycache__
setup: requirements.txt
	python3 -m venv venv
	./venv/bin/pip install -r requirements.txt