# Denna fil är endast till för att det ska gå att installera hehemaker.py.
from setuptools import setup, find_packages

setup(
    name='hehe-maker',
    version='1.0.1a',
    description='Ett enkelt kommandoverktyg för att sätta ihop PDF:er till HeHE',
    author='Emil Jonathan Eriksson',
    author_email='eje1999@gmail.com',
    packages=find_packages(),
    project_urls={
        'Source': 'https://github.com/ginger51011/hehe-maker'
    },
)