# CappyBlappyShop

## .env file structure:
```
SERVER_PORT = 
DOMAIN= 
STRIPE_API_SECRET_KEY=
DB_USER=
DB_PASSWORD=
DJANGO_SECRET_KEY=

EMAIL_HOST = 
EMAIL_PORT = 
EMAIL_HOST_USER = 
EMAIL_HOST_PASSWORD = 
```

## Requirements(temporal):
```
amqp==5.1.1
argon2-cffi==21.3.0
argon2-cffi-bindings==21.2.0
asgiref==3.5.2
async-timeout==4.0.2
billiard==3.6.4.0
celery==5.2.7
certifi==2022.9.24
cffi==1.15.1
charset-normalizer==2.1.1
click==8.1.3
click-didyoumean==0.3.0
click-plugins==1.1.1
click-repl==0.2.0
cryptography==38.0.4
Deprecated==1.2.13
Django==4.0.6
djangorestframework==3.14.0
hiredis==2.0.0
idna==3.4
kombu==5.2.4
mysql==0.0.3
mysqlclient==2.1.1
packaging==21.3
prompt-toolkit==3.0.32
pycparser==2.21
PyMySQL==1.0.2
pyparsing==3.0.9
python-dateutil==2.8.2
python-dotenv==0.21.0
pytz==2022.6
redis==4.3.4
requests==2.28.1
six==1.16.0
sqlparse==0.4.2
stripe==4.1.0
urllib3==1.26.12
vine==5.0.0
wcwidth==0.2.5
wrapt==1.14.1
```
## API Endpoints
Every endpoint supports OPTION so you can see the methods and required payload data.

#### api/products
Accepts: [GET]
Responds with: catalogue of product previews
* #### <product_pk>
Accepts: [GET]
Responds with: specified product preview from catalogue
#### api/product
Accepts: [GET]
Responds with: list of composite products(product itself, addon, discount, ...)
* #### <product_pk>/
Accepts: [GET]
Responds with: specified composite product
#### api/cart/
Accepts:[GET, POST - clears the cart]
* #### item/
Accepts: [POST]
Request: product id, addon id, count
Responds with: cart redirect
* * #### <item_pk>/
Accepts: [DELETE]
Responds with: cart redirect
#### api/account/
Accepts: [GET, PUT, PATCH]
Requests: See OPTION for detailed information
Responds with: GET - profile information, (PUT, PATCH) - redirect to GET
#### api/checkout/
Creates checkout session in Stripe and responds with url pointing towards Stripe checkout page
* #### success
* #### cancel
#### api/token/ [name='token_obtain_pair']
Accepts: [POST]
Requests: pair of registered user's name and password
Responds with: returns pair of access token and refresh token
#### api/token/refresh/ [name='token_refresh']
Accepts: [POST]
Requests: refresh token
Responds with: access token
#### api/token/verify/ [name='token_verify']
Accepts: [GET]
Responds with: if token is valid and unexpired
