# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

import os
import sys
sys.path.insert(0, os.path.abspath('../../'))


# -- Project information -----------------------------------------------------

project = 'Flask-Assistant'
copyright = '2021, Shinyhero36'
author = 'Shinyhero36'
project = author


# The full version, including alpha/beta/rc tags
release = '0.0.1'

# -- Global variables --------------------------------------------------------
rst_prolog = f"""
.. |project| replace:: **{project}**
"""

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",  # Google, Numpy style docstring
    "sphinx.ext.coverage",
    "sphinx_tabs.tabs",     # Tabs
]

templates_path = ['_templates']

exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# html_theme = 'alabaster'
# html_theme = "insegel"
html_theme = 'press'

html_static_path = ['_static']

html_title = "Hello World"
html_favicon = "_static/logo.svg"

html_show_sphinx = False

html_sidebars = {'**': [
    'util/searchbox.html',      # Searchbox
    'util/sidetoc.html',        # ToC
]}
html_css_files = ["css/custom.css"]
html_js_files = ['js/custom.js']

html_theme_options = {
  "external_links": [
      ("PyPI Releases", "https://pypi.org/"),
      ("Source Code", "https://github.com/Shinyhero36//"),
      ("Issue tracker", "https://github.com/Shinyhero36//issues")
  ]
}

