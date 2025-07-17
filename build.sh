#!/usr/bin/env bash

echo "Downloading TiDB CA cert..."
curl -o ca.pem https://download.pingcap.org/cacert.pem

echo "TiDB CA cert downloaded successfully."
