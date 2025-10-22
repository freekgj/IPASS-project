from setuptools import setup, find_packages

setup(
    name="mastermind_ai",
    version="0.1.0",
    author="Freek Gerrits Jans",
    author_email="freekgj@hotmail.com",
    description="A Mastermind game where AI guesses the code",
    packages=find_packages(),
    install_requires=[
        "numpy",
    ],
    python_requires='>=3.8',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
