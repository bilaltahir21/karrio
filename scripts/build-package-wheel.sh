#!/usr/bin/env bash

source "scripts/activate-env.sh"

echo "building wheel for" $1

export POETRY_PYPI_TOKEN_PYPI=${REGISTRY_TOKEN}

# access package
cd "$1" || exit 1

clean_build_files .

# build wheel
if [ -f "pyproject.toml" ]; then
    rm -f poetry.lock
    poetry update
    output=$(poetry build -f wheel 2>&1);
    r=$?;
else
    output=$(python setup.py bdist_wheel 2>&1);
    r=$?;
fi

# backup build files
backup_wheels . $2
clean_build_files .

cd - > /dev/null;

# Log build result output
if [[ ${r} -eq 1 ]]; then
    echo "> build "${1}" ${cross} \n ${output}"; exit ${r};
else
    echo "> build "${1}" ${check} ";
fi;

exit ${r};
