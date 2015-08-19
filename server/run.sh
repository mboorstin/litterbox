#!/bin/bash

if [ ! -f ./sqlite.db ]; then
  python project/populate_db.py
fi

nohup python project/app.py &
