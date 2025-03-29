.PHONY: test coverage clean lint format dev install

# Install development dependencies
dev:
    pip install -e ".[dev]"
    pip install pytest pytest-cov ruff black build

# Install package
install:
    pip install -e .

# Run all tests
test:
    pytest tests -v

# Run tests with coverage and open report
coverage:
    pytest --cov=teamcraft_api --cov-config=.coveragerc --cov-report=html
    xdg-open htmlcov/index.html || open htmlcov/index.html || echo "Open htmlcov/index.html manually."

# Remove caches and build artifacts
clean:
    find . -type d -name "__pycache__" -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete
    rm -rf .pytest_cache .coverage htmlcov dist build *.egg-info

# Run ruff linting
lint:
    ruff check teamcraft_api tests

# Format code using black
format:
    black teamcraft_api tests

# Build package
build:
    python -m build
