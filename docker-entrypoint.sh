#!/bin/bash


source venv/bin/activate

uvicorn backend-api/main:app --reload
