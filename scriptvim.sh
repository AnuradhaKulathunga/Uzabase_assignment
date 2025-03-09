#!/bin/bash

# Run the data processing scripts
python src/run.py process_data --cfg config/cfg.yaml --dataset news --dirout "zimp/data"
python src/run.py process_data_all --cfg config/cfg.yaml --dataset news --dirout "zimp/data"