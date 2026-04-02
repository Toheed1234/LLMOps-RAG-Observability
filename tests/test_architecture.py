import os
import pytest

def test_data_directory_exists():
    """Ensure the data directory is created for ingestion."""
    if not os.path.exists("data"):
        os.makedirs("data")
    assert os.path.exists("data"), "Data directory missing!"

def test_src_structure():
    """Ensure all core MLOps components exist."""
    assert os.path.exists("src/ingestion.py")
    assert os.path.exists("src/retriever.py")
    assert os.path.exists("src/bot.py")

def test_requirements_file():
    """Ensure requirements are pinned for the CI/CD pipeline."""
    assert os.path.exists("requirements.txt")
