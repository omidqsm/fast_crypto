# setup manual

### requirements
- **docker** and **docker compose**

### steps
- open a terminal window in the project folder
- run ```docker compose up --build```
- open **localhost:8000/docs/** in your browser

# how to test
- There are 3 crypto currencies hardcoded in the project which can
be seen in **_src/settings.py_** also minimum exchange value
is set to **10$**.
- on application startup three users are defined. for more info look at _**src/database.py**_ 

 
## sample curl:

curl -X 'POST' \
  'http://localhost:8000/trade' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": 2,
  "symbol": "ABAN",
  "amount": 1
}'

## notes
- this project is written in **FastAPI**