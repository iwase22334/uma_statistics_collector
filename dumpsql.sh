#!/bin/bash
mkdir -p /tmp/database
pg_dump -U postgres -h localhost -p 5433 \
-t n_race \
-t n_uma_race \
everydb2 > /tmp/database/statistics_source.sql
