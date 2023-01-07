#!/bin/bash

PY=python


if [ $1 = 'e' ]; then
  $PY exp.py
elif [ $1 = 'tgp' ]; then
  echo ""
else
  echo "Unexpected arg= ${1}"
fi
