#!/bin/sh

if [ -z "$1" ]; then
  echo "usage: myawesomescript.sh <bit.ly_url>" 1>&2
  exit 1
fi

url="$1"

case "$url" in
  http://*|https://*) ;;
  *) url="http://$url" ;;
esac

location=$(curl -sI "$url" | grep -i 'Location:' | cut -d' ' -f2)

if [ -z "$location" ]; then
  exit 1
fi

printf '%s\n' "$location"