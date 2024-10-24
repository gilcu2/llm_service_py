# IU Conding challenge

The proposed implementation uses llama3.2 for answer and kafka for the history.
Communication between the main api endpoint and the answer endpoint is done by http call. 

## Running:

./scripts/build_images.sh
docker-compose up

In other terminal:

curl -X POST -H "Content-Type: text/plain" --data "How are you llama" \
    http://localhost:8080/question_ollama

The history is:
curl  http://localhost:8083/history

but the connection to kafka from python inside the container is failing

## Testing

Implemented in pytest but are failing because of the dependencies with other services. 
For solving the dependent services have to be mocked. Also end 2 end tests have to be created.
