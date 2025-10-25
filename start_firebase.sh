#!/bin/sh

if [ ! -d firebase/data ]; then
  mkdir -p firebase/data
  echo 'create Directory: firebase/data'
fi

firebase emulators:start --project demo-project --import firebase/data --export-on-exit firebase/data &

