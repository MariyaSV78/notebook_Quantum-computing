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
  echo "Install it using:"
  echo "  sudo apt update && sudo apt install -y python3-venv"
  exit 1
fi

echo "--- Creating virtual environment ---"
if [ -d "$VENV_PREFIX" ]; then
  echo "Virtual environment already exists."
else
  echo "Creating a virtual environment..."
  python3 -m venv "$VENV_PREFIX"
fi

echo "--- Activating virtual environment ---"
source "$VENV_PREFIX/bin/activate"

echo "--- Using Python ---"
which python

echo "--- Upgrading pip ---"
python -m pip install --upgrade pip

echo "--- Installing Python packages ---"
if [ -f "$SCRIPTPATH/requirements.txt" ]; then
    python -m pip install -r "$SCRIPTPATH/requirements.txt"
else
    echo "No requirements.txt found at $SCRIPTPATH"
fi

echo "--- Installing/updating Jupyter kernel ---"
python -m pip install --upgrade ipykernel

# Remove old kernel if it exists
if jupyter kernelspec list | grep -q "^$VENV_NAME\s"; then
    echo "Removing existing kernel $VENV_NAME"
    jupyter kernelspec remove "$VENV_NAME" -f
else
    echo "No existing kernel $VENV_NAME found, skipping removal."
fi

# Register kernel
python -m ipykernel install \
    --user \
    --name "$VENV_NAME" \
    --display-name "Python ($VENV_NAME)"

echo "✅ Environment setup complete."
echo ""
echo "To use the environment, run:"
echo "source $VENV_PREFIX/bin/activate"
echo "jupyter lab"
