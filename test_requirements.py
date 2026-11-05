import sys
from pathlib import Path


def test_requirements_have_no_stdlib_modules():
    lines = Path(__file__).with_name("requirements.txt").read_text().split()
    assert not set(lines) & set(sys.stdlib_module_names)
