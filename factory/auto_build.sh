#!/bin/bash
set -euo pipefail

export PYTHONDONTWRITEBYTECODE=1
cd "$(dirname "$0")"
python3 ad.py
python3 test_gfwlist.py
python3 gfwlist.py
python3 build_confs.py
python3 generate_qrcode.py
python3 publications.py
