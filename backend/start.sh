#!/bin/bash
dotenv() {
  set -a
  [ -f .env ] && . .env
  set +a
}
dotenv
source $PATH_PYTHON
python main.py
deactivate