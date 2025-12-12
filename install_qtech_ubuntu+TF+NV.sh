#!/bin/bash

VENV_NAME="Quantum_Computing_venv"
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
VENV_PREFIX=$SCRIPTPATH/$VENV_NAME


echo "--- Checking python3-venv ---"

if python3 -m venv --help &>/dev/null; then
  echo "Python venv is already installed."
else
  echo "Attempting to install Python venv..."
  sudo apt -y update && sudo apt -y install python3-venv
  echo "Python venv has been installed."
fi


echo "--- Creating virtual environment ---"

if [ -d "$VENV_NAME" ]; then
    echo "Virtual environment '$VENV_NAME' exists for the project."
else
    echo "Creating a virtual environment"
    python3 -m venv "$VENV_NAME"
fi


echo "Activate the virtual environment"
source "$VENV_NAME"/bin/activate

echo "--- Installing Python packages ---"
pip3 install -r requirements.txt

echo "--- Installing Jupyter kernel ---"
python3 -m ipykernel install --user --name=$VENV_NAME

echo "--- Enabling classic notebook extensions ---"
python -m jupyter nbextension enable --py widgetsnbextension --sys-prefix
python -m jupyter nbextension enable --py ipympl --sys-prefix
python -m jupyter nbextension enable --py pythreejs --sys-prefix



