#!/bin/sh

if [ $# -ne 2 ]; then
    echo "Usage: ./toolwait <process name> <tool>"
    exit
fi

progstr=$1
tool=$2
progpid=`pgrep -o $progstr`
while [ "$progpid" = "" ]; do
    progpid=`pgrep -o $progstr`
done
$tool -p $progpid
