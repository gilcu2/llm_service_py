#!/bin/bash

docker build -t api-service -f api.Dockerfile .
docker build -t answer-service -f answer.Dockerfile .
docker build -t history-service -f history.Dockerfile .
#docker build -t ollama-service -f ollama.Dockerfile .