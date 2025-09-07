from pathlib import Path
from setuptools import setup

# Read the README.md for the long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name='caskada',
    version='2.2.0',
    py_modules=['caskada'],
    author="Victor Duarte",
    description="Minimalist AI framework in 300 Lines. Enable LLMs to Program Themselves.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://skada.ai/caskada/",
    license='MPL-2.0',
    classifiers=[
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
    ],
)
