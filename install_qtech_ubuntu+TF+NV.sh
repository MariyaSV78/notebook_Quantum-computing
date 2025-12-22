#!/bin/bash
set -e

VENV_NAME="Quantum_Computing_venv"
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
VENV_PREFIX="$SCRIPTPATH/$VENV_NAME"


echo "--- Checking python3-venv ---"

if python3 -m venv --help &>/dev/null; then
  echo "Python venv is already installed."
else
  echo "Python venv is not installed."
  echo "You can install it by running:"
  echo "  sudo apt update && sudo apt install -y python3-venv"
  exit 1
fi


echo "--- Creating virtual environment ---"
if [ -d "$VENV_PREFIX" ]; then
  echo "Virtual environment already exists."
else
  echo "Creating a virtual environment"
  python3 -m venv "$VENV_PREFIX"
fi

echo "--- Activating virtual environment ---"
source "$VENV_PREFIX/bin/activate"

echo "--- Using Python ---"
which python

echo "--- Installing Python packages ---"
echo "--- Installing Python packages ---"
if [ -f "$SCRIPTPATH/requirements.txt" ]; then
    python -m pip install -r "$SCRIPTPATH/requirements.txt"
else
    echo "No requirements.txt found at $SCRIPTPATH"
fi

echo "--- Installing Jupyter kernel ---"
python -m pip install --upgrade ipykernel
python -m ipykernel install \
  --user \
  --name "$VENV_NAME" \
  --display-name "Python ($VENV_NAME)"

# echo "--- Enabling classic notebook extensions ---"
# python -m jupyter nbextension enable --py widgetsnbextension --sys-prefix
# python -m jupyter nbextension enable --py ipympl --sys-prefix
# python -m jupyter nbextension enable --py pythreejs --sys-prefix

echo "✅ Environment setup complete."
echo "You can now run:"

echo "source $VENV_PREFIX/bin/activate"
echo "jupyter lab"

