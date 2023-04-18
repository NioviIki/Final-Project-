#!/usr/bin/env sh

set -o errexit

cmd="$*"

postgres_ready () {
  sh "docker/wait-for-command.sh" -t 5 -s 0 52 -c "curl $DB_HOST:$DB_PORT"
}

until postgres_ready; do
  >&2 echo 'Postgres is unavailable - sleeping'
done

>&2 echo "Postgres is up - continuing ..."

exec $cmd