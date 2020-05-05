

import setuptools


with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="glasswall-aws-product-test-automation",
    version="0.0.1",
    author="AngusWR",
    author_email="aroberts@glasswallsolutions.com",
    description="A small package for testing Glasswall AWS products",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/filetrust/aws-product-test-automation",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
    ],
    python_requires='>=3.6',
)
