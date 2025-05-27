#!/bin/bash

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Installing local package in development mode..."
pip install -e .

echo "Installing greenlet (required for SQLAlchemy async)..."
pip install greenlet

 