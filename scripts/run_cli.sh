#!/usr/bin/env bash
set -euo pipefail
python -m shop_assistant.main --query "${1:-best laptop for CS student under 900}" --save-json
