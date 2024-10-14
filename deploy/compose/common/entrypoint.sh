#!/bin/bash

set -o errexit
set -o pipefail

# Let the DB start
python -m a8t_tools.db.wait_for_db

alembic upgrade head

# Create superuser
if [ -n "${EMAIL}" ]; then
  python manage.py create-superuser "${FIRSTNAME}" "${LASTNAME}" "${EMAIL}" "${PASSWORD}" || true
fi

exec "$@"