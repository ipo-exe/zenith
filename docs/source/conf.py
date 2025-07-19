import sys
from pathlib import Path

# Allow sphinx to find the package
sys.path.insert(0, str(Path("..", "src").resolve()))

# Enable autodoc using type hinting annotations
autodoc_typehints = "description"

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'zenith'
copyright = '2025, Iporã Brito Possantti'
author = 'Iporã Brito Possantti'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
]

templates_path = ['_templates']
exclude_patterns = []

language = 'en'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']


import os
print(f"Current working directory: {os.getcwd()}")
print(f"sys.path before insert: {sys.path}")
print(f"Resolved src path: {str(Path('..', 'src').resolve())}")
