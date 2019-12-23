# Denna fil är endast till för att det ska gå att installera hehemaker.py.
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_descrtiption = fh.read()

setup(
    name='hehe-maker',
    version='1.1.2a',
    author='Emil Jonathan Eriksson',
    author_email='eje1999@gmail.com',
    description='Ett enkelt kommandoverktyg för att sätta ihop PDF:er till HeHE',
    long_descrtiption=long_descrtiption,
    long_description_content_type="text/markdown",
    scripts=["hehemaker"],  # Lets us run via pipx
    url="https://github.com/ginger51011/hehe-maker",
    packages=find_packages(),
)