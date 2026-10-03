#!/bin/bash

host=$1

if [[ "_$host" == "_" ]]; then
  echo "usage: $0 <hostname or ip>"
  exit 1
fi

if [[ ! -f ~/.ssh/alumno.key ]]; then
  mkdir -p ~/.ssh
  cp `dirname $0`/claves/alumno.key ~/.ssh
  chmod 600 ~/.ssh/alumno.key
fi

ssh -i ~/.ssh/alumno.key -o 'StrictHostKeyChecking no' alumno@$1
