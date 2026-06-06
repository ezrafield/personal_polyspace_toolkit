#!/usr/bin/env sh
set -eu

input=$(cat)

printf "%s" "$input" | grep -Eiq '(BEGIN (RSA|OPENSSH|PRIVATE) KEY|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9_]{30,}|sk-[A-Za-z0-9]{20,})' && {
  echo "Blocked output that looks like a secret." >&2
  exit 1
}

printf "%s" "$input"
