# Bucket List Service API

[![Build Status](https://semaphoreci.com/api/v1/stanmd/bucketlist/branches/feature-review/badge.svg)](https://semaphoreci.com/stanmd/bucketlist) [![Coverage Status](https://coveralls.io/repos/github/NdagiStanley/bucketlist/badge.svg?branch=feature-review)](https://coveralls.io/github/NdagiStanley/bucketlist?branch=feature-review) [![Code Issues](https://www.quantifiedcode.com/api/v1/project/413c57d2358940f097221a243f88d224/badge.svg)](https://www.quantifiedcode.com/app/project/413c57d2358940f097221a243f88d224) [![Code Climate](https://codeclimate.com/github/NdagiStanley/bucketlist/badges/gpa.svg)](https://codeclimate.com/github/NdagiStanley/bucketlist) [![Issue Count](https://codeclimate.com/github/NdagiStanley/bucketlist/badges/issue_count.svg)](https://codeclimate.com/github/NdagiStanley/bucketlist) [![Code Health](https://landscape.io/github/NdagiStanley/bucketlist/feature-review/landscape.svg?style=flat)](https://landscape.io/github/NdagiStanley/bucketlist/feature-review)

![Checkpoint Status](https://img.shields.io/badge/Andela%20@Stan__MD-CP%202%20complete-green.svg)

> Be able to **CRUD** bucketlists

BLiSA is a simple REST API allowing users to _**C**REATE_ bucketlists (things you want to do before you expire) and items in them. Then they are able to _**R**EAD_, _**U**PDATE_ and _**D**ELETE_ them.

It's implementing:

![Flask, python, mysql](http://codehandbook.org/wp-content/uploads/2015/07/python_ff.jpg)
(Image courtesy- codehandbook.org)

## Installation
**We'll use the terminal here**

1. Clone the repo
run: ```git clone https://github.com/NdagiStanley/bucketlist.git```

2. Create a virtual environment using [virtualenv](https://virtualenv.readthedocs.org/en/latest/) or [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/)
3. In the virtual environment install DEPENDENCIES
RUN ```pip install -r requirements.txt```

## Task 0

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

## Task 1

Implement Token Based Authentication

| EndPoint      |   Public Access   |
| ---- |:----: |
| POST /auth/login  |  TRUE     |
| POST /auth/register   |  TRUE     |
| POST /bucketlists/    |  FALSE    |
| GET /bucketlists/     |  FALSE    |
| GET /bucketlists/< id >   |   FALSE   |
| PUT /bucketlists/< id >   |   FALSE   |
| DELETE /bucketlists/< id >    |   FALSE   |
| POST /bucketlists/< id >/items/   |   FALSE   |
| PUT /bucketlists/< id >/items/< item_id >     |   FALSE   |
| DELETE /bucketlists/< id >/items/< item_id >      |   FALSE   |

The responses all belong to the logged in user

## Task 2

Implement Pagination on the API

Adding `?limit=20` to the bucketlists endpoint to specify the number of results returned.

The limit is edittable via the url but set the **default as 20** and **maximum as 100**

- [http://localhost:5000/bucketlists?limit=20](http://localhost:5000/bucketlists?limit=20) (**GET**)

Pagination is also implemented.

The following will return the second page after limiting results to the default 20 per page

- [http://localhost:5000/bucketlists?page=2](http://localhost:5000/bucketlists?page=2) (**GET**)

Here is an example of pagination with custom limit. The results are 10 per page and we have requested the second page

- [http://localhost:5000/bucketlists?limit=10&page=2](http://localhost:5000/bucketlists?limit=10&page=2) (**GET**)

## Task 3

Implement Searching by name

Adding `?q=bucket1` to the bucketlists endpoint to specify characteristics of results returned.

- [http://localhost:5000/bucketlists?q=bucket1](http://localhost:5000/bucketlists?q=bucket1) (**GET**)
- [http://localhost:5000/bucketlists?q=bucket1](http://localhost:5000/bucketlists?q=bucket1) (**GET**)

In this case expected results are Bucket lists with the string "**bucket1**" in their name
`?q=b` will return Bucket lists with the string "**b**" in their name including those with the string "**b**", "**bu**", "**buc**", "**buck**" and so on.

## Running

RUN `python api/manage.py start` to create the db and tables to be used

RUN `python api/manage.py runserver` and go the pages at:

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

The token will be used in all subsequent requests. Otherwise the requests will be unauthorised.

In Postman enter the token in the header like this: (NB: The Content-Type is necessary in GET and PUT methods)



In **POST** the body should be in this format:
```json
{
  "name": "Travel"
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

or either:

```json
{
  "title": "Travel to Mombasa"
}
```

```json
{
  "done": true
}
```

RUN `python api/manage.py exit` to exit from the API


## Testing

RUN `nosetests`

RUN `coverage run tests.py`

For both tests and coverage
RUN `nosetests --with-coverage`

---
Copyright AD-2016
###### [Stanley Ndagi](http://techkenyans.org/jamii/stanmd) c/o [Andela](http://andela.com)
