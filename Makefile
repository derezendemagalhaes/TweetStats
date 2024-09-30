PYTHON=python3.11
VENV=venv
ACTIVATE=$(VENV)/bin/activate

.PHONY: run

$(VENV)/bin/activate: requirements.txt
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV)
	@echo "Installing dependencies..."
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements.txt

run: $(ACTIVATE)
	@echo "Running the application..."
	. $(ACTIVATE); python src/main.py

.PHONY: clean
clean:
	rm -rf $(VENV)
	@echo "Virtual environment removed."
