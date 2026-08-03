#!/bin/bash
source ~/.venv/bin/activate
python add_toc.py "$@"
deactivate