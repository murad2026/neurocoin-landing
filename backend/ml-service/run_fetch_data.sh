#!/bin/bash
source "$(dirname \"$0\")/venv/bin/activate"
python "$(dirname \"$0\")/fetch_data.py" >> "$(dirname \"$0\")/logfile.log" 2>&1
