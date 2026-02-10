#!/bin/bash
set -e

# Name of the Conda environment folder inside your project
ENV_NAME="conda_env"

# Path to your project folder (script is in project folder)
PROJECT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
ENV_PATH="$PROJECT_DIR/$ENV_NAME"
ENV_FILE="$PROJECT_DIR/environment.yml"

echo "📂 Project folder: $PROJECT_DIR"
echo "🛠 Conda environment path: $ENV_PATH"

# Check if conda is available
if ! command -v conda &> /dev/null
then
    echo "❌ Conda not found. Please install Miniconda or Anaconda first."
    exit 1
fi

# Create environment.yml if it doesn't exist
if [ ! -f "$ENV_FILE" ]; then
    echo "Creating environment.yml..."
    cat > "$ENV_FILE" << EOL
name: Quantum_Project
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.11
  - numpy
  - scipy
  - matplotlib
  - pandas
  - scikit-learn
  - seaborn
  - pillow
  - ipywidgets
  - ipympl
  - pythreejs
  - notebook
  - jupyterlab
  - pip
  - pip:
      - nb_mypy
      - plotly
      - jupyterlab_mathjax2
      - widgetsnbextension
      - qiskit
      - qiskit-aer
      - qiskit-nature
      - qiskit-ibm-runtime
      - qiskit-serverless
      - qiskit-ibm-catalog
      - pylatexenc
EOL
    echo "✅ environment.yml created."
else
    echo "environment.yml already exists."
fi

# Create or update Conda environment
if conda env list | grep -q "$ENV_PATH"; then
    echo "Environment exists, updating..."
    conda env update --prefix "$ENV_PATH" --file "$ENV_FILE" --prune
else
    echo "Creating Conda environment..."
    conda env create --prefix "$ENV_PATH" --file "$ENV_FILE"
fi


# Activate environment
echo "Activating environment..."
conda activate "$ENV_PATH"

# Upgrade pip in the environment
python -m pip install --upgrade pip setuptools wheel

# Register Jupyter kernel
KERNEL_NAME="Quantum_Computing_conda"
if jupyter kernelspec list | grep -q "^$KERNEL_NAME\s"; then
    echo "Removing existing kernel $KERNEL_NAME..."
    jupyter kernelspec remove "$KERNEL_NAME" -f
fi

echo "Registering Jupyter kernel..."
python -m ipykernel install --user --name "$KERNEL_NAME" --display-name "Python ($KERNEL_NAME)"

echo "✅ Conda environment setup complete!"
echo "To use it:"
echo "  conda activate $ENV_PATH"
echo "  jupyter lab"
