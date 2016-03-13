# Bucket List Service API

[![Build Status](https://semaphoreci.com/api/v1/stanmd/bucketlist/branches/feature-create-api/badge.svg)](https://semaphoreci.com/stanmd/bucketlist) [![Coverage Status](https://coveralls.io/repos/github/NdagiStanley/bucketlist/badge.svg?branch=feature-create-API)](https://coveralls.io/github/NdagiStanley/bucketlist?branch=feature-create-API) [![Code Issues](https://www.quantifiedcode.com/api/v1/project/413c57d2358940f097221a243f88d224/badge.svg)](https://www.quantifiedcode.com/app/project/413c57d2358940f097221a243f88d224) [![Code Climate](https://codeclimate.com/repos/56ceebeb477c416148009caa/badges/28e40e636cc883cc20c5/gpa.svg)](https://codeclimate.com/repos/56ceebeb477c416148009caa/feed) [![Issue Count](https://codeclimate.com/repos/56ceebeb477c416148009caa/badges/28e40e636cc883cc20c5/issue_count.svg)](https://codeclimate.com/repos/56ceebeb477c416148009caa/feed)

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

##Running
RUN `cd sqlalchemy_orm` to get to the *sqlalchemy_orm directory*
RUN `python api.py start` to create the db and tables to be used
RUN `python api.py runserver` and go the pages at:

- [http://localhost:5000/](http://localhost:5000/) (index page)
- [http://localhost:5000/bucketlists/](http://localhost:5000/bucketlists/) endpoints (GET, POST)
- [http://localhost:5000/bucketlists/1](http://localhost:5000/bucketlists/1) endpoints (GET, PUT, DELETE)
- [http://localhost:5000/bucketlists/1/items/](http://localhost:5000/bucketlists/1/items/) endpoints (POST)
- [http://localhost:5000/bucketlists/1/items/1](http://localhost:5000/bucketlists/1/items/1) endpoints (PUT, DELETE)

RUN `python api.py exit` to exit from the API


##Testing

RUN `nosetests`

RUN `coverage run tests.py`

For both tests and coverage
RUN `nosetests --with-coverage`

---
Copyright AD-2016
###### [Stanley Ndagi](http://techkenyans.org/jamii/stanmd) c/o [Andela](http://andela.com)
