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
    # Readers can view the actual Python source of your functions/classes/modules directly from the docs.
    # Especially useful for open-source or public APIs.
    'sphinx.ext.viewcode',

    'sphinx.ext.githubpages',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'en'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

# For autodoc to find the package
import sys
from pathlib import Path

sys.path.insert(0, str(Path('..', 'src').resolve()))

# For autodoc to use the type hinting
autodoc_typehints = "description"
