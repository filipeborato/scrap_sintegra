## Project Structure

Project related to the Technical Challenge – Squad “Melhorias Estruturantes”. The project has a Python API with a route that creates a Task, sends a CNPJ to a RabbitMQ queue, and returns a Task ID. The Worker/Consumer listens on that queue; when it receives a message, it scrapes the data and saves it in Redis, updating the task’s status. A separate API route lets you fetch the processed data.

## How It Works

The project uses 4 containers:

1. `rabbitmq`: Container running RabbitMQ for messaging.  
2. `worker`: Container responsible for the messaging “Consumer”.  
   - Note: uses Supervisor to spawn consumers and manage process count.  
3. `api`: API container handling routes via FastAPI.  
4. `redis`: Container for the cache system using Redis.  

## Starting the Project via Container

To start the project in containers, follow these steps:

1. Clone the project  
    ```sh
    git clone https://github.com/filipeborato/{project_name}
    ```
2. Enter the project folder  
    ```sh
    cd {project_name}/
    ```
3. Set folder permissions  
    ```sh
    chmod o+w * -R
    ```
4. Bring up the containers  
    ```sh
    docker-compose up
    ```
   – Note: wait until all containers are up  
5. Verify the containers  
    ```sh
    docker-compose ps
    ```

## Access and Routes

- Access RabbitMQ web UI:  
  `http://localhost:15672/` or `http://{IPVM}:15672/` (if applicable)  
  user: `crawler` | password: `rabbit`  
- Access Redis CLI:  
  ```sh
  docker exec -it redis redis-cli
- Route (POST) /scrape: `http://localhost:8000/scrape`
```sh
{
    "cnpj": "00012377000160"
}
```
- Curl example:
```sh
curl --location --request POST 'http://localhost:8000/scrape' \
--header 'Content-Type: application/json' \
--data-raw '{
    "cnpj": "00012377000160"
}'
```
- Route (GET) /results/{task_id}: `http://localhost:8000/results/{task_id}`
- Run API tests: `docker exec -it api pytest`

## Notes
I added Supervisor to launch the consumer, so I don’t have to call the script directly or set up a cron job, plus I get more logs and can easily scale the number of consumers (the project currently uses 2). There are some “duplicated” files, but I did that assuming they’re separate services.
Comandos docker-compose:

- docker-compose build: only builds the images used by the containers
- docker-compose start: starts the containers
- docker-compose stop: stops the containers
- docker-compose restart: restarts the containers
- docker-compose ps: lists the containers
- docker-compose up:  creates and starts the containers
- docker-compose down: stops and removes the containers
- docker-compose logs:  shows the containers’ logs
- docker-compose scale:  sets the number of replicas for a given service
