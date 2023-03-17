from pathlib import Path
from setuptools import find_namespace_packages, setup


NAME = "qa-chat"
VERSION = 0.1
PACKAGES = find_namespace_packages()

HERE = Path(__file__).absolute().parent
INSTALL_REQUIRES = (HERE / "requirements.txt").read_text().split("\n")
LICENSE = (HERE / "LICENSE").read_text()

def install_pkg():
    setup(
        version=VERSION,
        description="QA CLI tool leveraging LLMs",
        author="steffens21",
        author_email="steffens21@gmail.com",
        license=LICENSE,
        python_requires=">=3.9.0",
        install_requires=INSTALL_REQUIRES,
        include_package_data=True,
        zip_safe=False
    )

if __name__ == "__main__":
    install_pkg()

