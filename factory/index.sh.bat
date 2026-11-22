#!/bin/bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
cd "$(dirname "$0")"
python3 ad.py
python3 build_confs.py
