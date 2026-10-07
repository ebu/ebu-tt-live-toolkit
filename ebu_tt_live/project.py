"""
Expose project variables into python code and documentation
"""
import os
import tomllib

# When building documentation, don't assume we're in the root folder
path = os.path.dirname(__file__)
ebu_tt_live_dir = os.path.dirname(path)
project_toml_path = os.path.join(ebu_tt_live_dir, "pyproject.toml")
with open(project_toml_path, "rb") as f:
    _META = tomllib.load(f)

name = _META["project"]["name"]
version = _META["project"]["version"]
description = _META["project"]["description"]
