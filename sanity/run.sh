#!/usr/bin/env bash


if [[ $# -eq 0 ]] ; then
    echo 'please specify language to check'
    exit 0
fi

docker-compose up -d
sleep 20
open http://localhost:9643?api_key=ticktok-zY3wpR
cd $1
sh ./start.sh

