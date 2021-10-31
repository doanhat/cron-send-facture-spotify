#!/bin/bash
# shellcheck disable=SC2039
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  # shellcheck disable=SC2006
  TOMORROW=`date -d 'tomorrow' +%d`
elif [[ "$OSTYPE" == "darwin"* ]]; then
  # shellcheck disable=SC2006
  TOMORROW=`date -v+1d +%d`
fi
# See if tomorrow's day is some day
if [ "$TOMORROW" -eq 01 ]; then
	# shellcheck disable=SC2164
	# shellcheck disable=SC2046
	# TODO : export thread_in in environment variable type number
	/usr/local/bin/docker run -e USER_EMAIL_ADDRESS="$FB_USER_EMAIL_ADDRESS" -e USER_PASSWORD="$FB_USER_PASSWORD" -e THREAD_ID=6947468915279299 cron-send-facture-spotify:latest
	exit
else
  echo "Tomorrow is not 01"
fi