# IU Coding challenge

The proposed implementation uses llama3.2 for answer.
For keep the history I think the best option is Kafka because scalability but, I didn't achieve 
that the Python client works inside the container. So I did another implementation with postgress.
Communication between the main api endpoint and the answer endpoint is done by http call. 

## Running:

./scripts/build_images.sh
docker-compose up

In other terminal for send a question:

curl -X POST -H "Content-Type: text/plain" --data "How are you llama" \
    http://localhost:8080/question_ollama

For gte the history:

curl  http://localhost:8083/history

### Example

```shell

reynaldo.gila$  curl -X POST -H "Content-Type: text/plain" --data "How are you llama" http://localhost:8080/question_ollama
{
  "question":"How are you llama",
  "answer":"I'm doing well, thank you for asking! I'm a large language model, so I don't have feelings or emotions like humans do, but I'm always happy to chat with you and help with any questions or topics you'd like to discuss. How about you? How's your day going?"
}
```


## Testing

Tests were implemented in pytest but are failing because of the dependencies between services. 
For solving this problem the dependent services have to be mocked. 
Also end 2 end tests have to be created.
