@echo off
set CMD=%1

if "%CMD%"=="test" (
    pytest tests
) else if "%CMD%"=="coverage" (
    pytest tests --cov=teamcraft_api --cov-report=html
    start htmlcov\index.html
) else if "%CMD%"=="clean" (
    echo Cleaning Python cache files...
    for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
    echo Cleaning .pyc files...
    del /s /q *.pyc >nul 2>&1
    echo Cleaning build artifacts...
    if exist "htmlcov" rd /s /q htmlcov
    if exist ".pytest_cache" rd /s /q .pytest_cache
    if exist ".coverage" del /q .coverage
    if exist "dist" rd /s /q dist
    if exist "build" rd /s /q build
    if exist "teamcraft_api.egg-info" rd /s /q teamcraft_api.egg-info
    echo Clean complete!
) else if "%CMD%"=="package" (
    python -m build
) else (
    echo Available commands:
    echo    make test       Run all tests
    echo    make coverage   Run tests with HTML coverage report
    echo    make clean      Remove caches and build artifacts
    echo    make package    Build the PyPI wheel and sdist (requires 'build')
)
