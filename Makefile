.PHONY: verify test mypy

# Pre-release verification harness — wire coverage + live read sweep +
# field-drop audit + helper coverage. Live layers need SMALLEST_API_KEY.
verify:
	python scripts/verify.py

# Static checks (mirror CI)
mypy:
	mypy .

test:
	pytest -rP -n auto .
