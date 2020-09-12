# Payment Gateway
This app is a mock for payment gateway service
## Quickstart

To work in a sandboxed Python environment it is recommended to install the app in a Python [virtualenv](https://pypi.python.org/pypi/virtualenv).

1. Clone and install dependencies

    ```bash
    $ git clone https://github.com/akanuragkumar/payment-gateway.git
    $ cd payment-gateway
    $ pip install -r requirements.txt
    $ cd payments
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
## Assumptions:
1. The PaymentMethod table contains payment type-(i.e- debit card, credit card) and curreny(i.e- USD, Euro). This is required as we can add as many payment type and currency we are currently supporting. It is a non- editable field and we can only disable it by setting the is_active to false. Here type denotes-(currency or payment_type) and subtype denotes-(euro, creditcard, usd, debitcard).
2. For making payment, we first check whether type and currency both are present and in active state in PaymentMethod table.
3. We have made an assumption that card number digit should always be equal to 16, so if the card number digit is less than or greater than 16, it throws error.
4. We check whether the card has expired or not by checking the year and month. In month field we can give- 9 or 09, both the cases have been handled.
5. Here we have used random function for generating success or failure for the payment. In real scenario it would depend on number of cases like account balance etc.
6. We have also done schema validation in place for json field 'card'.
7. Float formatting in place for amount field while returning the response from API to remove trailling zeros.
8. For authorization code we are using UUID4 and it is an indexed primary key in PaymentDetail table.

### [Link for screenshots of API response](https://github.com/akanuragkumar/payment-gateway/tree/master/screenshots)   
## API Documentation 

### `This Endpoint takes payment type and payment currency and stores it for validation` 

1. `POST /api/payment-method` 

```json
 application/json - {
    "type":"payment_type",
    "subtype":"debitcard"
}
```
##### `response`

```json
{
    "type": "payment_type",
    "subtype": "debitcard"
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

##### `response`

```json
{
    "type": "debitcard",
    "currency": "Euro",
    "amount": 500,
    "card": {
        "number": 4111111111111111
    },
    "status": "success",
    "authorization_code": "6b50138f-bd91-4c49-a7c9-01d3f5baff6f",
    "time": "2020-09-06 12:11:43"
}
```    


