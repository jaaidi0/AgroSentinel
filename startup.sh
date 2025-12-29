#!/bin/bash
cd python_worker
gunicorn --bind=0.0.0.0:5000 --timeout 600 --workers=2 main:app
