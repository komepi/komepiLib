from setuptools import setup, find_packages

setup(
    name = "komepiLib",
    version = "0.1",
    packages=find_packages(),
    extras_require={
        "develop":["selenium"]
    }
)