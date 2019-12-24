#!/bin/bash

db_dir=/tmp/uma_statistics_01
db_name=stat_src.sql

mkdir -p ${db_dir}
pg_dump \
-t n_uma_race \
-t n_race \
everydb2 > ${db_dir}/${db_name}
