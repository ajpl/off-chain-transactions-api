# Off Chain Transactions API

This is a toy django project that simulates off chain transactions.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pipenv.

```bash
pip install pipenv
```
Then install dependencies using pipenv
```bash
pipenv install
```

## Run server

```bash
pipenv run python manage.py runserver
```

## Documentation
Every endpoint requires authentication. Authentication is handled by using JWTs and sent to the server via Bearer tokens on requests' headers.

- `/api/token/`
  - POST
    - response: `{"access": ..., "refresh": ...}`
    - data:`{"username": "test", "password": "12345"}`
  
- `/api/token/refresh/`
  - POST
    - response: `{"access": ...}`
    - data: `{"refresh": ...}`
- `/api/balances/`
  - GET
    - response: `{[Balance]}`
  - POST
    - response: `Balance`
    - data: `{"ticker": "ETH"}`
- `/api/balances/:id/`
  - GET
    - response: `Balance`
- `/api/balance-entries`
  - GET
    - response: `[BalanceEntry]`
  - POST
    - response: `BalanceEntry`
    - data: `{"balance": Balance.id, "tx_amount": 1, "tx_type": 1}`
      - tx_type
        - 1: Airdrop
        - 2: Burn
        - 3: P2P
          - Requires: `to_balance: Balance.id` extra field in request data
- `/api/balance-entries/:id/`
  - GET
    - response: `BalanceEntry`

## Run tests
Install dev dependencies with:

```bash
pipenv install --dev
```

Run tests with:
```bash
pipenv run pytest
```

### Install precommit hooks

[Pre commit hooks](https://pre-commit.com/) run useful linters (black, flake8) before comitting code.
```bash
pip install pre-commit
pre-commit install
```



## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[Apache License 2.0](https://choosealicense.com/licenses/apache-2.0/)
