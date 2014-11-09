#!/bin/bash

ROOT=$(readlink -f $(dirname ${BASH_SOURCE[0]})/.. )
DB=$ROOT/db.sqlite3
MANAGE=$ROOT/manage.py
ACTIVATE=$ROOT/venv/bin/activate

rm -f $DB
source $ACTIVATE
$MANAGE migrate
$MANAGE createsuperuser --noinput --username=y --email=yordan@4web.bg
# Now a superuser is created with no password set
$MANAGE shell <<EOF
from django.contrib.auth.models import User
user = User.objects.get(username='y')
user.set_password('1234')
user.save()
EOF
