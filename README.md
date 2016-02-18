# Bucket List Service API
[![Build Status](https://semaphoreci.com/api/v1/stanmd/bucketlist/branches/feature-create-API/badge.svg)](https://semaphoreci.com/stanmd/bucketlist)
[![Code Issues](https://www.quantifiedcode.com/api/v1/project/413c57d2358940f097221a243f88d224/snapshot/origin:feature-create-API:HEAD/badge.svg)](https://www.quantifiedcode.com/app/project/413c57d2358940f097221a243f88d224)

BLiSA is a simple REST API allowing users to _CREATE_ bucketlists (things you want to do before you expire) and items in them. Then they are able to _VIEW_, _UPDATE_ and _DELETE_ them. It's implementing:

![Flask, python, mysql](http://codehandbook.org/wp-content/uploads/2015/07/python_ff.jpg)
(Image courtesy- codehandbook.org)

##Installation
**We'll use the terminal here**
1. Clone the repo
run: ```git clone https://github.com/NdagiStanley/bucketlist.git```

2. Create a virtual environment using [virtualenv](https://virtualenv.readthedocs.org/en/latest/) or [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/)
3. In the virtual environment install DEPENDENCIES
run: ```pip install -r requirements.txt```

##Testing

##Documentation
The documentation for the final API is in this [Apiary API Blueprint](http://docs.stanmdbucketlist.apiary.io/)

You could also perform tests on this repo using the API blueprint by running the following commands:

- `npm install -g dredd`
This command installs _dreed_ which will help us run the tests
Incase of any errors, please try running this command again as root/Administrator `sudo npm install -g dredd`

- `dredd init -r apiary -j apiaryApiKey:th3@p1@ryK3y -j apiaryApiName:stanmdbucketlist`

- `pip install dredd_hooks`
Run this command in the virtual environment. You could run it globally if you wish (that is if you reckon you'll use apiary's API blueprint amny times over)

- `dredd apiary.apib http://localhost:5000 --language python --hookfiles=./hooks*.py`
Run this command after running the server

---
Copyright (c) 2016
###### [Stanley Ndagi](http://techkenyans.org/jamii/stanmd) c/o [Andela](http://andela.com)