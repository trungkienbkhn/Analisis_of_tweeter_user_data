#!/bin/bash
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 's';"
sudo -u postgres psql -c "CREATE DATABASE function1;"
sudo -u postgres psql -c "CREATE DATABASE function2;"
python3 Connector/function1/CreateTable/table.py
python3 Connector/function1/CreateTable/Copy.py
python3 Connector/function2/CreateTable/tablecn2.py
python3 Connector/function2/CreateTable/copycn2.py
