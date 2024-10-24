# IU Conding challenge

The proposed implementation use llama3.2 for answer and kafka for the history.
Communication between the main api endpoint and the answer endpoint is done by http call 

## Running:

./scripts/build_images.sh
docker-compose up

In other terminal:

curl -X POST -H "Content-Type: text/plain" --data "How are you llama" \
    http://localhost:8080/question_ollama

The history must is:
curl  http://localhost:8083/history

but the connection to kafka from python inside the container is failing

## Test

Implemented in pytest but are failing because the dependencies with other services. 
The dependent services have to be mocked. End 2 end services have to be created.
