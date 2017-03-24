# Contribution Guidelines

This document is designed to get you setup to contribute to this repository.
There are two ways to help out: you can help out in the python aggregator that
fetches and parses facebook posts, or you can help out in the RPC server.

## Python Aggregator

You need to setup a virtual environment for the best development experience.

1. Set up a python virtual environment.
2. Install the packages detailed in requirements.txt using pip

	```sh
	pip install -r requirements.txt
	```
3. Make changes, and as you go, keep testing.

Some details about what each file of importance does:

* post.py : acts as a model. Makes database schema and creates a new
  table if there isn't one already.
* db_service.py : takes care of postgres communication
* aggregator.py : this is the workhorse file, which fetches and parses posts
* post_reader.py : contains a parser for posts (non trivial)
* runner.py : runs stuff in an infinite loop

## RPC Server

1. You need to have node and npm installed for this.
2. Install the node modules needed, and run it.

	```sh
	cd RPCServer
	npm install
	node RPCServer.js
	```

3. That's it! Edit the RPCServer.js file to contribute.
