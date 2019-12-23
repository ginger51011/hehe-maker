# Denna fil är endast till för att det ska gå att installera hehemaker.py.
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_descrtiption = fh.read()

setup(
    name='hehe-maker',
    version='1.1.1',
    description='Ett enkelt kommandoverktyg för att sätta ihop PDF:er till HeHE',
    author='Emil Jonathan Eriksson',
    author_email='eje1999@gmail.com',
    packages=find_packages(),
    project_urls={
        'Source': 'https://github.com/ginger51011/hehe-maker'
    },
)