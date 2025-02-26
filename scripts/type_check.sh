#!/usr/bin/env sh

TO_CHECK="
api_service
history_service
llm_service
common
tests/
"

#pyright $TO_CHECK
mypy $TO_CHECK
