from setuptools import find_packages, setup
from typing import List


def get_requirements(file_path: str) -> List[str]:
    """
    Returns a cleaned list of install requirements.
    Ignores editable installs (-e .)
    """
    with open(file_path, "r") as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.strip() for req in requirements if req.strip() and not req.startswith("-e")]
    return requirements


setup(
    name="mlproject",
    version="0.0.1",
    author="Md Shahid",
    author_email="shahidsmohammed47@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt"),
)
# This setup script is used to package the ML project as a Python module.