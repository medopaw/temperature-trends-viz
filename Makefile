.PHONY: help install install-dev run clean format lint type-check test all-checks

# Default target
help:
	@echo "Temperature Trends Viz - Development Commands"
	@echo "============================================="
	@echo ""
	@echo "Available commands:"
	@echo "  install      - Install production dependencies"
	@echo "  install-dev  - Install development dependencies"
	@echo "  run          - Run the application"
	@echo "  clean        - Clean up generated files"
	@echo "  format       - Format code with black and isort"
	@echo "  lint         - Run flake8 linter"
	@echo "  type-check   - Run mypy type checker"
	@echo "  test         - Run tests with pytest"
	@echo "  all-checks   - Run all code quality checks"
	@echo ""
	@echo "Quick start:"
	@echo "  make install-dev && make run"

# Install production dependencies
install:
	uv sync

# Install development dependencies
install-dev:
	uv sync --extra dev

# Run the application
run:
	uv run streamlit run weather_gui.py

# Clean up generated files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .mypy_cache/

# Format code
format:
	uv run black weather_gui.py
	uv run isort weather_gui.py

# Run linter
lint:
	uv run flake8 weather_gui.py

# Run type checker
type-check:
	uv run mypy weather_gui.py

# Run tests
test:
	uv run pytest

# Run all code quality checks
all-checks: format lint type-check
	@echo "✅ All code quality checks passed!"

# Development workflow
dev: install-dev all-checks run
