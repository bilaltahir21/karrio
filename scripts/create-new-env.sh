#!/usr/bin/env bash

# Source environment variables
source "scripts/_env.sh"

# prepare virtual environment directory
echo 'prepare env directory ...'
deactivate >/dev/null 2>&1
mkdir -p "${ROOT:?}/$ENV_DIR"

[[ -d "${ROOT:?}/$ENV_DIR/$BASE_DIR" ]] && rm -rf "${ROOT:?}/$ENV_DIR/$BASE_DIR"

# create virtual environment
echo "creating $BASE_DIR env ..."
python3 -m venv "${ROOT:?}/$ENV_DIR/$BASE_DIR"

echo "activating $BASE_DIR env ..."
source "${ROOT:?}/$ENV_DIR/$BASE_DIR/bin/activate"

# install requirements
echo "installing base requirements ..."
pip install pip --upgrade

if [[ "$*" != *--empty* ]]; then
    pip install -r "${ROOT}/requirements.dev.txt"
fi
