# Denna fil är endast till för att det ska gå att installera hehemaker.py.
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_descritiption = fh.read()

setup(
    name='hehe-maker',
    version='1.3.11',
    author='Emil Jonathan Eriksson',
    author_email='eje1999@gmail.com',
    description='A simple command line tool to modify papers in PDF format. Can also create new articles from PDF(s).',
    long_description=long_descritiption,
    long_description_content_type="text/markdown",
    url="https://github.com/ginger51011/hehe-maker",
    packages=find_packages(),
    entry_points={  # Tells python what to run
        "console_scripts": [
            "hehemaker = hehemaker.hehemaker:main"   # Name of console script
        ]
    },
    install_requires=[      # So that pip also installs pdfrw
          "pdfrw",
          "pdfminer",
          "markovify",
      ],
)