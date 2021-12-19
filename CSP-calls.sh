#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
python3 CSPStowage.py $DIR/CSP-tests cells-00.txt containers-00.txt
python3 CSPStowage.py $DIR/CSP-tests cells-00.txt containers-01.txt
python3 CSPStowage.py $DIR/CSP-tests cells-01.txt containers-00.txt
python3 CSPStowage.py $DIR/CSP-tests cells-01.txt containers-01.txt
