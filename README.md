# LLM service

LLM microservices with ollama, postgress

## Running:

./scripts/export_requirements.sh
./scripts/build_images.sh
docker-compose up

In other terminal for send a question:

curl -X POST -H "Content-Type: application/json" -d '{"question":"Who are you"}' \
    http://localhost:8080/question

For gte the history:

curl  http://localhost:8080/history/

## Testing (after docker-compose up)

pytest