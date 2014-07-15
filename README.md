pyro
====

Symantec Endpoint Protection (SEP) computer status export parser, which will upload parsed data to CouchDB (NoSQL) database.

## About
Computer status export from SEP contains a lot of data. Some of the fileds seems valuable. Some of them don't. For ease of use and ability to specifiy particular queries to the database, I've created a script that will parse the csv export file, create a json structure of my choosing, and upload the documents to the CouchDB database. Each document has an id created from the hostname of the computer. Update to the specific computer/document must contain a previous revision ID. 

## Example execution...
... will look like that:

![Pyro example execution](https://raw.githubusercontent.com/mnmnc/img/master/pyro1.jpg)

## Video recording...
... of execution can be viewed [here (webm file)](https://raw.githubusercontent.com/mnmnc/img/master/out2.webm).

### Usage

Either:

  - python3 pyro.py filename.csv

or

  - ./pyro.py filename.csv

### Variables
You should change the values in the line 375:

  `couch = MyCouch( "1.0.0.2", "7777", "username", "password", "database_name")`
