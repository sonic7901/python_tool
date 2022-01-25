#!/bin/sh

CUR=`pwd`

mkdir report

cd /wappalyzer

python3 main.py $URL

if [ $? -ne 0 ]; then { echo "Failed, aborting." ; exit 1; } fi

if [ ! -f "data.json" ]; then
    echo "{}" >> data.json
fi

cp *.json $CUR/report

cd $CUR

zip -r report.zip report
