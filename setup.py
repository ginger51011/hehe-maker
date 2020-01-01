# Denna fil är endast till för att det ska gå att installera hehemaker.py.
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_descritiption = fh.read()

setup(
    name='hehe-maker',
    version='1.2.2',
    author='Emil Jonathan Eriksson',
    author_email='eje1999@gmail.com',
    description='Ett enkelt kommandoverktyg för att sätta ihop PDF:er till HeHE | A simple command line tool to modify papers in PDF format',
    long_description=long_descritiption,
    long_description_content_type="text/markdown",
    url="https://github.com/ginger51011/hehe-maker",
    packages=find_packages(),
    entry_points={  # Tells pipx what to do
        "console_scripts": [
            "hehemaker=hehemaker.__main__:main"   # Must be underscore
        ]
    },
    install_requires=[      # So that pip also installs pdfrw
          "pdfrw",
          "pdfminer",
          "morkovify",
      ],
)