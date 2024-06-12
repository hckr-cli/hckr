# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'hckr'
copyright = '2024, Ashish'
author = 'Ashish'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx_click',
    # other extensions...
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
html_theme = 'shibuya'
html_static_path = ['_static']

# TODO: enhance it https://shibuya.lepture.com/install/

html_theme_options = {
    # "announcement": "The content of the announcement",
    "color_mode": "light",  # light or dark
    "github_url": "https://github.com/pateash/hckr",
    "discussion_url": "https://github.com/pateash/hckr/discussions",
}

html_context = {
    "source_type": "github",
    "source_user": "pateash",
    "source_repo": "hckr",
    "source_version": "main",  # Optional
    "source_docs_path": "/docs/source",  # Optional
}
