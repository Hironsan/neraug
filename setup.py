import io
import os
import sys

from setuptools import find_packages, setup

# Package meta-data.
NAME = "neraug"
DESCRIPTION = "Data augmentation tool for named entity recognition"
URL = "https://github.com/Hironsan/neraug"
EMAIL = "hiroki.nakayama.py@gmail.com"
AUTHOR = "Hironsan"
LICENSE = "MIT"

here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = "\n" + f.read()

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel upload")
    sys.exit()

required = ["seqeval"]

setup(
    name=NAME,
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(exclude=("tests",)),
    install_requires=required,
    include_package_data=True,
    license=LICENSE,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
