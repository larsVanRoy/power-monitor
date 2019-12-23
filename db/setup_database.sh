#!/usr/bin/env bash

PGPASSWORD=postgres psql -d postgres -U postgres -f ./create_database.sql
PGPASSWORD=admin psql -d youlessmonitor -U youlessadmin -f ./schema.sql
