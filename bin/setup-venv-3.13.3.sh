#!/usr/bin/env bash
# Create a Python 3.13.3 virtual environment at .venv3.13.3
# Usage: ./bin/setup-venv-3.13.3.sh

set -euo pipefail

VENV_DIR=".venv3.13.3"

# Try common python executables
CANDIDATES=("python3.13" "python3.13.3" "python3" "python")
FOUND=""

for cmd in "${CANDIDATES[@]}"; do
  if command -v "$cmd" >/dev/null 2>&1; then
    ver=$($cmd -c 'import sys; print(".".join(map(str, sys.version_info[:3])))') || true
    if [[ "$ver" == "3.13.3" ]]; then
      FOUND="$cmd"
      break
    fi
  fi
done

if [[ -z "$FOUND" ]]; then
  echo "Python 3.13.3 not found on PATH."
  echo "The script will try to use pyenv if available, or you can install Python 3.13.3 via your package manager."
  echo
  echo "Options:"
  echo "  1) Install with pyenv (recommended):"
  echo "     curl https://pyenv.run | bash"
  echo "     exec $SHELL -l"
  echo "     pyenv install 3.13.3"
  echo "     pyenv local 3.13.3"
  echo "     ./bin/setup-venv-3.13.3.sh"
  echo
  echo "  2) On macOS using Homebrew (if available):"
  echo "     brew install python@3.13" 
  echo "     ln -s /opt/homebrew/opt/python@3.13/bin/python3.13 ~/bin/python3.13  # adjust path as needed"
  echo
  echo "If you already have Python 3.13.3 installed under a different name, re-run the script with that executable on the PATH."
  exit 0
fi

echo "Found Python interpreter: $FOUND"

# Create venv
if [[ -d "$VENV_DIR" ]]; then
  echo "Virtualenv already exists at $VENV_DIR"
else
  echo "Creating virtualenv at $VENV_DIR using $FOUND"
  $FOUND -m venv "$VENV_DIR"
  echo "Created venv. Activating and upgrading pip..."
  # shellcheck disable=SC1090
  source "$VENV_DIR/bin/activate"
  pip install --upgrade pip setuptools wheel
  echo "Virtualenv ready at $VENV_DIR"
fi

# Display quick activation instructions
cat <<EOF
To activate the venv in this shell:

  source $VENV_DIR/bin/activate

Then install dev requirements (if present):

  pip install -r requirements.txt

EOF
