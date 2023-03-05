# CappyBlappyShop
## Overview
Not every part of the functionality from *webapp* implementation is done in REST, and vice versa
! This repository represents only *RESTful api* part of the site! The *webapp* implementation is stored in CappyBlappyShop (https://github.com/HCodeKeeper/CappyBlappyShop) ! (it's separated as branching is a little messed up)\
This is a shop that sells capybaras. *RESTful* part is written in python using drf, redis, mysql, stripe integration, JWT. Celery is integrated but not used in this version (whereas webapp uses its functionality)
## What was implemented
- authorization (JWT): registration, login and password update. Using django mailing library and celery for sending authorization token asynchronously. The token is sent to your email and temporarily saved in redis to be compared with your input and then erased.
- page caching (django using redis)
- result pagination (drf)
- profile customizing
- cart (django session, redis)
- checkout and payment (stripe integration).
## What a user can do
On this site you can:
- add to cart
- checkout your cart
- search products
- register
- update password
- login
- see random offers
- update profile info
- specify addons (services and additional products served by the seller) and quantity when adding a product in the cart

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
