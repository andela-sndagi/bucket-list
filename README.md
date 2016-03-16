# Bucket List Service API

[![Build Status](https://semaphoreci.com/api/v1/stanmd/bucketlist/branches/feature-create-api/badge.svg)](https://semaphoreci.com/stanmd/bucketlist) [![Coverage Status](https://coveralls.io/repos/github/NdagiStanley/bucketlist/badge.svg?branch=feature-create-API)](https://coveralls.io/github/NdagiStanley/bucketlist?branch=feature-create-API) [![Code Issues](https://www.quantifiedcode.com/api/v1/project/413c57d2358940f097221a243f88d224/badge.svg)](https://www.quantifiedcode.com/app/project/413c57d2358940f097221a243f88d224) [![Code Climate](https://codeclimate.com/github/NdagiStanley/bucketlist/badges/gpa.svg)](https://codeclimate.com/github/NdagiStanley/bucketlist) [![Issue Count](https://codeclimate.com/github/NdagiStanley/bucketlist/badges/issue_count.svg)](https://codeclimate.com/github/NdagiStanley/bucketlist)

BLiSA is a simple REST API allowing users to _**C**REATE_ bucketlists (things you want to do before you expire) and items in them. Then they are able to _**R**EAD_, _**U**PDATE_ and _**D**ELETE_ them.
In short you are able to **CRUD** bucketlists

It's implementing:

![Flask, python, mysql](http://codehandbook.org/wp-content/uploads/2015/07/python_ff.jpg)
(Image courtesy- codehandbook.org)

##Installation
**We'll use the terminal here**

1. Clone the repo
run: ```git clone https://github.com/NdagiStanley/bucketlist.git```

2. Create a virtual environment using [virtualenv](https://virtualenv.readthedocs.org/en/latest/) or [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/)
3. In the virtual environment install DEPENDENCIES
RUN ```pip install -r requirements.txt```

##Task

Implement the API in this structure:

```json
{
  "id": 1,
  "name": "BucketList1",
  "items": [
    {
      "id": 1,
      "title": "I need to do X",
      "date_created": "2015-08-12 11:57:23",
      "date_modified": "2015-08-12 11:57:23",
      "done": false
    }
  ],
  "date_created": "2015-08-12 11:57:23",
  "date_modified": "2015-08-12 11:57:23",
  "created_by": "1113456"
}
```

##Running

RUN `cd sqlalchemy_orm` to get to the *sqlalchemy_orm directory*

RUN `python api.py start` to create the db and tables to be used

RUN `python api.py runserver` and go the pages at:

- [http://localhost:5000/](http://localhost:5000/) index page (**GET**)
- [http://localhost:5000/auth/register/](http://localhost:5000/auth/register/) signup page (**POST**)
```json
{
  "username": "user1",
  "password": "p@ssw0rd",
  "conf_password": "p@ssw0rd"
}
```
- [http://localhost:5000/auth/login/](http://localhost:5000/auth/login/) login page (**POST**)
```json
{
  "username": "user1",
  "password": "p@ssw0rd"
}
```
This returns a token in this format:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ1ODEwNjkyMCwiaWF0IjoxNDU4MTAzMzIwfQ.eyJpZCI6Nn0.irPIrqstGIupCD428dtSOxV8zzwm5IgoCLpTsk-oH5k"
}
```
- [http://localhost:5000/bucketlists/](http://localhost:5000/bucketlists/) endpoints (**GET**, **POST**)
Preferably use curl in this manner in the terminal:

```
curl -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ1ODEwNjUwOCwiaWF0IjoxNDU4MTAyOTA4fQ.eyJpZCI6Nn0.Ekt_3nmlzJokR-exLg7uwiRrbUFPFB0LMAk2J_mJ0MI:unused -i -X GET http://127.0.0.1:5000/bucketlists/
```
The token will be used in all subsequent requests. Otherwise the requests will be unauthorised.

In **POST** the body should be in this format:
```json
{
  "name": "Travel",
  "created_by": "user1"
}
```
- [http://localhost:5000/bucketlists/1](http://localhost:5000/bucketlists/1) endpoints (**GET**, **PUT**, **DELETE**)
the body for **PUT** here is same as the above body :point_up_2:
- [http://localhost:5000/bucketlists/1/items/](http://localhost:5000/bucketlists/1/items/) endpoints (**POST**)

In the format below:
```json
{
  "title": "Travel"
}
```
- [http://localhost:5000/bucketlists/1/items/1](http://localhost:5000/bucketlists/1/items/1) endpoints (**PUT**, **DELETE**)

In **PUT** the body should be in this format:
```json
{
  "title": "Travel to Mombasa",
  "done": true
}
```

RUN `python api.py exit` to exit from the API


##Testing

RUN `nosetests`

RUN `coverage run tests.py`

For both tests and coverage
RUN `nosetests --with-coverage`

---
Copyright AD-2016
###### [Stanley Ndagi](http://techkenyans.org/jamii/stanmd) c/o [Andela](http://andela.com)
