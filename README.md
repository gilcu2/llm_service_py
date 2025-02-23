# LLM service

LLM service with logging additional login endpoint

## Running:

./scripts/build_images.sh
docker-compose up

In other terminal for send a question:

curl -X POST -H "Content-Type: text/plain" --data "Who are you" \
    http://localhost:8080/question_ollama

For gte the history:

curl  http://localhost:8083/history/




## Testing

