"""
Pytest configuration for UI/UX Pro Max tests.
"""
import pytest
import sys
from pathlib import Path

# Add scripts directory to Python path
scripts_dir = Path(__file__).parent.parent
sys.path.insert(0, str(scripts_dir))


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers": "integration: mark test as integration test")


@pytest.fixture(scope="session")
def data_dir():
    """Provide path to the data directory."""
    return scripts_dir.parent / "data"


@pytest.fixture(scope="session")
def products_csv(data_dir):
    """Load products.csv rows."""
    import csv
    
    products_path = data_dir / "products.csv"
    with open(products_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


@pytest.fixture(scope="session")
def colors_csv(data_dir):
    """Load colors.csv rows."""
    import csv
    
    colors_path = data_dir / "colors.csv"
    with open(colors_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


@pytest.fixture(scope="session")
def styles_csv(data_dir):
    """Load styles.csv rows."""
    import csv
    
    styles_path = data_dir / "styles.csv"
    with open(styles_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


@pytest.fixture(scope="session")
def catalog_summary(data_dir):
    """Load catalog-summary.json."""
    import json
    
    summary_path = data_dir / "catalog-summary.json"
    with open(summary_path, encoding='utf-8') as f:
        return json.load(f)
