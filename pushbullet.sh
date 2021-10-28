#!/bin/bash

API="o.LXAe15oQcGGn6fRXE3hLqQ4qAEheONUn"
MSG="$1"

curl -u $API: https://api.pushbullet.com/v2/pushes -d type=note -d title="Alert" -d body="$MSG"
