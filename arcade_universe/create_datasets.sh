#!/bin/bash -x

jobdispatch python premade_pento64x64.py --seed 12312555 --no-of-exs 20000 --bg-texture-type plain --out-file-name pento64x64_20k &
jobdispatch python premade_pento64x64.py --seed 12193885 --no-of-exs 20000 --bg-texture-type plain --out-file-name pento64x64_20k &

