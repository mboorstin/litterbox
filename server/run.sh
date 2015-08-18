#!/bin/bash

if [ ! -f ./sqlite.db ]; then
  python project/populate_db.py
fi

python project/app.py
