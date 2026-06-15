#!/usr/bin/env bash
set -euo pipefail
python -m skilltokenx \
  --root examples/input \
  --out runs/demo \
  --target-reduction 0.35 \
  --mode safe \
  --overwrite
