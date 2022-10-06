import sys

try:
    from skbuild import setup
except ImportError:
    print(
        "Please update pip, you need pip 10 or greater,\n"
        " or you need to install the PEP 518 requirements in pyproject.toml yourself",
        file=sys.stderr,
    )
    raise

from setuptools import find_packages

setup(
    name="cppsort",
    version="0.0.2",
    description="a minimal example package (with pybind11)",
    author="Henry Schreiner",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    cmake_install_dir="src/cppsort",
    include_package_data=True,
    extras_require={"test": ["pytest"]},
    python_requires=">=3.8",
    cmake_args=['-G=Visual Studio 16 2019'] # cmake generator  https://cmake.org/cmake/help/v3.6/manual/cmake.1.html#options
)