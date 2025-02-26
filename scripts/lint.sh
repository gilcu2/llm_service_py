#!/usr/bin/env sh

TO_CHECK="
api_service
history_service
llm_service
common
tests/
"

flake8 $TO_CHECK
