from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="tkbase64",  # Required
    version="0.0.1",  # Required
    description="Tkinter GUI to encode & decode base64 strings.",  # Optional
    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",  # Optional (see note above)
    author="parklez",  # Optional
    classifiers=[  # Optional
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="tkinter, base64",  # Optional
    packages=find_packages(),  # Required
    python_requires=">=3.7, <4",
    entry_points={
        'console_scripts': [
            'tkbase64=tkbase64.main:App'
        ]
    },
    project_urls={  # Optional
        "Bug Reports": "https://github.com/parklez/tkbase64/issues",
        "Source": "https://github.com/parklez/tkbase64",
    },
)