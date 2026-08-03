#!/bin/bash
cd "$(dirname "$0")"
source .venv/bin/activate
python3 pdf_to_png_gui.py
