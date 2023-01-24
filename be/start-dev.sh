#!/bin/bash
cd src
export MODE="DEVELOPMENT"
uvicorn index:app --reload
cd ..
