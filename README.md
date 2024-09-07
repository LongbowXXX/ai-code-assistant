# ai-code-assistant
Code implementation assistance by LLM.

## Installation
```
$ pip install -e .
$ pip install -e .[dev]
```

## Run GUI
```
$ mesop src/ai_code_assistant/gui/gui_app.py
```
## mypy
```
$ mypy . --no-incremental
```
## flake8
```
$ flake8 --statistics
```
## black
```
$ black .
```

## pytest
```
$ pytest --html=build/reports/test/result/report.html --cov --cov-report=html:build/reports/test/coverage --cov-report=term
```
