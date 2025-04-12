from pathlib import Path
from setuptools import setup

# Read the README.md for the long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name='brainyflow',
    version='0.2.0',
    py_modules=['brainyflow'],
    author="Victor Duarte",
    description="Minimalist AI framework in 65 Lines. Enable LLMs to Program Themselves.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://flow.brainy.sh",
)
