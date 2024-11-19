# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = 'Material Simulations - TFYA99'
copyright = '2024, joabe712 fabfi969 kaljo229 pauka833'
author = 'joabe712, fabfi969, kaljo229, pauka833'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

    # "sphinx.ext.todo",
    # "sphinx.ext.viewcode",

extensions = [
    'sphinx.ext.viewcode',
    'sphinxcontrib.apidoc',
    ]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['static']

apidoc_module_dir = '../'
apidoc_output_dir = 'reference'
apidoc_excluded_paths = ["tests"]
apidoc_separate_modules = True
apidoc_template_dir = './templates'