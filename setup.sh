#!/bin/bash

pushd `dirname $0`  # ensure the cwd is the script's directory


echo "Setting up Python Environment"

python3 -m venv env
source env/bin/activate

echo "Installing Python Requirements"

pip install -r requirements.txt

deactivate

echo "Installing Other Requirements"
wget "https://gist.githubusercontent.com/netj/526585/raw/7f7cd17541a1d29bc978eccc80c270ab6b83ed9c/memusg" -O scripts/memusg


popd
