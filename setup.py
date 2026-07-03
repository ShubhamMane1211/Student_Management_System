from setuptools import setup, find_packages

def get_requirements(file_path):
    with open(file_path) as f:
        requirements = f.read().splitlines()

    if "-e ." in requirements:
        requirements.remove("-e .")

    return requirements


setup(
    name="Student_Management_System",
    version="0.0.1",
    author="Shubham Mane",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt"),
)