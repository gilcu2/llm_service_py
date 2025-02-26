#!/bin/bash

PARALLELISM=${1:-4}
#TIMEOUT="--timeout=60 --timeout_method=thread"
TIMEOUT="--timeout=60 --timeout_method=signal"

TEST_DIRS="tests"

pytest -ra $TIMEOUT --durations=0 -n $PARALLELISM --dist loadgroup $TEST_DIRS
