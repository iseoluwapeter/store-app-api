#!/usr/bin/env bash

echo "Downloading TiDB CA cert..."
curl -o ca.pem https://download.pingcap.org/cacert.pem

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Build complete."
