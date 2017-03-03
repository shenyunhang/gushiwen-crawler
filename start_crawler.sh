#!/bin/bash

set -e
set -x

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DATA_DIR="${DIR}/data"

if [ -d ${DATA_DIR} ]
then
	rm -r ${DATA_DIR}
fi

time python ${DIR}/main.py
