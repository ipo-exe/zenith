# Tell Sphinx where your code is
import os
import sys
import pprint # debug

sys.path.insert(0, os.path.abspath('../src'))
#for x in os.walk('../src'):
#  sys.path.insert(0, x[0])
pprint.pprint(sys.path)

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Zenith'
copyright = '2025, Juliano & Iporã'
author = 'Juliano & Iporã'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",  # enables docstring parsing
    "sphinx.ext.napoleon", # Google-style / NumPy-style docstrings
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']


