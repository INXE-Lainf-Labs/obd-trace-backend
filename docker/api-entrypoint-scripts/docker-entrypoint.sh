#!/bin/bash
set -e

if [ "$1" = "migrate" ]
then
    # Migrations
    alembic upgrade head
elif  [ -n "$1" ]; then
    exec "$@"
fi

if [ $# -eq 0 ]
then
    OPTIONS=""
    if [ "$ENV" = "development" ] ; then
        python -u src/config/db_health_check.py
        OPTIONS="--reload"
    fi
    uvicorn src.main:app --host 0.0.0.0 $OPTIONS
fi
