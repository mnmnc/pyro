pyro
====

Symantec Endpoint Protection (SEP) computer status export parser, which will upload parsed data to CouchDB (NoSQL) database.

### About
Computer status export from SEP contains a lot of data. Some of the fileds seems valuable. Some of them don't. For ease of use and ability to specifiy particular queries to the database, I've created a script that will parse the csv export file, create a json structure of my choosing, and upload the documents to the CouchDB database. Each document has an id created from the hostname of the computer. Update to the specific computer/document must contain a previous revision ID. 

### Example execution...
... will look like that:

![Pyro example execution](https://raw.githubusercontent.com/mnmnc/img/master/pyro1.jpg)

### Database document
Each computer will be represented by document within CouchDB database. It will have a following structure:

```{
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
}```

### Video recording...
... of execution can be viewed [here (webm file)](https://raw.githubusercontent.com/mnmnc/img/master/out2.webm).

### Usage

Either: `python3 pyro.py filename.csv` or `./pyro.py filename.csv`

### Variables
You should change the values in the line 375:

  `couch = MyCouch( "1.0.0.2", "7777", "username", "password", "database_name")`

### Customization

I presume one might have different demands from the script and would want to load different values to the database. You can modify the functuon from line 191 `build_dictionary_structure` to create your own JSON structure.
