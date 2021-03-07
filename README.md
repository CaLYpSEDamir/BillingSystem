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