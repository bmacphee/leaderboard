#!/bin/bash
LOCAL_MODE=1 python manage.py collectstatic
zip -r static static
#aws s3 sync --acl public-read static s3://serverless-django-leaderboard/static/
