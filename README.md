# payment-gateway
This app is a mock for payment gateway service
## Quickstart

To work in a sandboxed Python environment it is recommended to install the app in a Python [virtualenv](https://pypi.python.org/pypi/virtualenv).

1. Clone and install dependencies

    ```bash
    $ git clone https://github.com/akanuragkumar/payment-gateway.git
    $ cd payment-gateway
    $ pip install -r requirements.txt
    ```

2. Running app

   ```bash
   $ python manage.py makemigrations payment_api
   $ python manage.py migrate
   $ python manage.py runserver
   ``` 
3. Running the unit test cases

   ```bash
   $ python manage.py test payment_api
   ``` 
### [Link for screenshots of API response](https://github.com/akanuragkumar/payment-gateway/tree/master/screenshots)   
## API Documentation 

### `This Endpoint takes payment type and payment currency and stores it for validation` 

1. `POST /api/payment-method` 

```json
 application/json - {
    "type":"payment_type",
    "subtype":"Debit card"
}
```
##### `response`

```json
{
    "type": "payment_type",
    "subtype": "Debit card"
}   
```
2. `GET /api/payment-method` 

##### `response`

```json
[
    {
        "type": "currency",
        "subtype": "Euro",
        "is_active": true
    },
    {
        "type": "payment_type",
        "subtype": "debitcard",
        "is_active": true
    }
]
```    

### `This Endpoint takes the payment details and returns appropriate response ` 

1. `POST /api/payment-detail` 

##### `response`

```json
 application/json - {
    "currency":"Euro",
    "type":"debitcard",
    "amount":500,
    "card":{
"number": 4111111111111111,
"expirationMonth": 2,
"expirationYear": 2020,
"cvv": 111
    }   
}
```



