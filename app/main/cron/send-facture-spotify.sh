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
	python app/main/send-facture.py
	exit
fi