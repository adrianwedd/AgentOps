import os
import sys

sys.path.insert(0, os.path.abspath("../.."))

project = "Agentic Index"
author = "OpenAI"
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon"]
html_theme = "furo"

autodoc_typehints = "description"
autodoc_mock_imports = ["pydantic"]
