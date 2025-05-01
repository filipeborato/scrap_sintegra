## Scrap Sintegra

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
    git clone https://github.com/filipeborato/scrap_sintegra
    ```
2. Enter the project folder  
    ```sh
    cd scrap_sintegra/
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

## Access and Routes

- **Access RabbitMQ Web UI:**  
  `http://localhost:15672/` or `http://{IPVM}:15672/` (if applicable)  
  Username: `crawler` | Password: `crawler`

- **Access Redis CLI:**  
  ```sh
  docker exec -it redis redis-cli
  ```

- **Route (POST) /scrape:** `http://localhost:8000/scrape`  
  **Payload Example:**
  ```json
  {
      "cnpj": "00012377000160"
  }
  ```
  **cURL Example:**
  ```sh
  curl --location --request POST 'http://localhost:8000/scrape' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "cnpj": "00012377000160"
    }'
  ```

- **Route (GET) /results/{task_id}:** `http://localhost:8000/results/{task_id}`  
  **cURL Example:**
  ```sh
  curl --location --request GET 'http://localhost:8000/results/1b84980b37370d59_20241108034959'
  ```

- **Run API Tests:**  
  ```sh
  docker exec -it api sh -c "PYTHONPATH=/usr/src/app pytest"
  ```
