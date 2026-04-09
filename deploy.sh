#!/bin/bash
git clone $1 && cd $(basename $1 .git)
bash setup_shizuku.sh && python3 tv_shizuku.py
