#!/bin/bash

sh -c uvicorn api_service.api_service:app --host "0.0.0.0" --port 8080 &
#uvicorn answer_service.answer_service:app --host "0.0.0.0" --port 8082 &
#uvicorn history_service.history_service:app --host "0.0.0.0" --port 8083 &