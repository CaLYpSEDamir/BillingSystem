### Billing System

A simple rest api project emulating money transferring between users.

```
1) Starting project:
    - docker-compose up
    - config file: payment/docker/env
```

```
2) API documentation: 
    - http://127.0.0.1:8000/docs
    - http://127.0.0.1:8000/redoc
```

```
3) Tools:
    - FastApi
    - Kafka
    - Postgresql
```

```
4) Logic:
    - User makes adding money transaction to his balance or transferring money transaction to other user.
    - All transactions are saved in db and sent to kafka broker.
    - Asynchronous broker consumer reads transactions from topic and updates users balances.
```

```
5) Scenario:
    - Create 2 users:
        - curl -X POST "http://127.0.0.1:8000/users/" -H "Content-Type: application/json" -d "{\"name\":\"A\"}"
        - curl -X POST "http://127.0.0.1:8000/users/" -H "Content-Type: application/json" -d "{\"name\":\"B\"}"
    
    - Add 100 money to user A:
        - curl -X POST "http://127.0.0.1:8000/users/1/add_money/" -H  "Content-Type: application/json" -d "{\"amount\":100}"
    
    - Transfer 50 money from user A to user B:
        - curl -X POST "http://127.0.0.1:8000/users/1/transfer_money/" -H "Content-Type: application/json" -d "{\"amount\":50,\"to_user\":2}"

    - Check balances of users. Must be 50 of user A and 50 of user B:
        - curl -X GET "http://127.0.0.1:8000/users/1/balance/"
        - curl -X GET "http://127.0.0.1:8000/users/2/balance/"
    
    - Check history of users transactions:
        - curl -X GET "http://127.0.0.1:8000/users/1/history/"
        - curl -X GET "http://127.0.0.1:8000/users/2/history/"
```