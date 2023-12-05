#!/bin/bash

py_version=$(python3 --version)
version_number=$(echo $py_version | cut -d' ' -f2)

pyenv virtualenv $version_number music_proj_env
pyenv local music_proj_env
pip install --upgrade pip

pip install -r requirements.txt

pyenv activate music_proj_env
