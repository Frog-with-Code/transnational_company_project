import os
import sys
sys.path.insert(0, os.path.abspath("../../src"))


project = 'Transnational company'
copyright = '2025, Artem Shumilov'
author = 'Artem Shumilov'
release = '1.0.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = []

language = 'en'

html_theme = 'alabaster'
html_static_path = ['_static']