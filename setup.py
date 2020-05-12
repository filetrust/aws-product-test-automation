

import os
import setuptools
from s93_test_automation import __version__


with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="glasswall-aws-product-test-automation",
    version=__version__,
    author="AngusWR",
    author_email="aroberts@glasswallsolutions.com",
    description="A small package for testing Glasswall AWS products",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/filetrust/aws-product-test-automation",
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "s93_test_automation = s93_test_automation.__main__:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.22.0"
    ],
)
