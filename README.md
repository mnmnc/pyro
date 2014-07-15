pyro
====

Symantec Endpoint Protection (SEP) computer status export parser, which will upload parsed data to CouchDB (NoSQL) database.

### About
Computer status export from SEP contains a lot of data. Some of the fileds seems valuable. Some of them don't. For ease of use and ability to specifiy particular queries to the database, I've created a script that will parse the csv export file, create a json structure of my choosing, and upload the documents to the CouchDB database ([installation instructions for Debian 7](https://raw.githubusercontent.com/mnmnc/config_repo/master/db/couchdb.txt)). Each document has an id created from the hostname of the computer. Update to the specific computer/document must contain a previous revision ID. 

### Example execution...
... will look like that:

![Pyro example execution](https://raw.githubusercontent.com/mnmnc/img/master/pyro1.jpg)

or if you prefer live preview here is a [webm file](https://raw.githubusercontent.com/mnmnc/img/master/out2.webm).


### Database document
Each computer will be represented by document within CouchDB database. It will have a following structure:

```
{
   "_id": "SomeComputerName",
   "_rev": "1-5e897671493625c4429e7f4679731a10",
   "osnet": {
       "current_login_domain": "LocalComputer",
       "os": "Windows Server 2008 R2 Standard Edition",
       "cn": "SomeComputerName",
       "domain": "local.domain.com",
       "free_space": "4000 MB",
       "user": "mnmnc",
       "city": "Atlanta",
       "ip": "10.0.0.101"
   },
   "vir": {
       "infected": "No",
       "policy_version": "1.1.410",
       "worst_detect": "No detections",
       "client_version": "10.1.1111",
       "revision": 2,
       "definition_version": 1405116000
   },
   "date": {
       "last_download": 1405288811,
       "timestamp": 1405310393,
       "last_virus": 0,
       "report_date": 1405288800,
       "last_status_change": 1405310393,
       "last_scan": 1404793803
   }
}
```

If you update the particular document, the previous versions of it will be available under previous revision numbers.
You can get all those numbers by querying database either by URL or by command line.
After navigating to url `http://user:pass@localhost:7777/database/document_id?revs_info=true` you will get json output that will contain:
```
"_revs_info":[
	{"rev":"4-6104f686dd699fb5ed015fab75b1bac5","status":"available"},
	{"rev":"3-7a2d436767eee419f94b086b071a6a6c","status":"available"},
	{"rev":"2-09209338dc434a3f7d0d9aea88d5e533","status":"available"},
	{"rev":"1-ab4d3fc74b8c50733fa7a5cae30238ce","status":"available"}
]
```


### Usage

Either: `python3 pyro.py filename.csv` or `./pyro.py filename.csv`

### Variables
You should change the values in the line 375:

  `couch = MyCouch( "1.0.0.2", "7777", "username", "password", "database_name")`

### Customization

I presume one might have different demands from the script and would want to load different values to the database. You can modify the functuon from line 191 `build_dictionary_structure` to create your own JSON structure.
