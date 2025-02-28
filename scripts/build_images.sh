#!/bin/bash

#docker build -t ollama-service -f ollama.Dockerfile .
docker build -t llm-service -f llm-service.Dockerfile .
docker build -t history-service -f history-service.Dockerfile .
docker build -t api-service -f api-service.Dockerfile .
docker build -t kafka-service -f kafka-service.Dockerfile .
