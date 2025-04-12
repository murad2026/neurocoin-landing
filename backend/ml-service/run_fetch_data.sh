#!/bin/bash
source /Users/Apple/Downloads/neurocoin-final-fixed/backend/ml-service/venv/bin/activate
python /Users/Apple/Downloads/neurocoin-final-fixed/backend/ml-service/fetch_data.py >> /Users/Apple/Downloads/neurocoin-final-fixed/backend/ml-service/logfile.log 2>&1

