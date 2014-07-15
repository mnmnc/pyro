#!/usr/bin/env python3

import csv 											# PARSING CSV
import time 										# TIMESTAMPS
import datetime 									# DATE CONVERSIONS
import sys 											# INTERACTION WITH SYSTEM
import os 											# OS SPECIFIC MODULE
import json 										# CONVERTING LISTS TO JSON
import pycouchdb 									# INTERACTIONS WITH COUCHDB
from colorama import init, Fore, Back, Style 		# COLORFUL PRINTING

class Computer:
	""" CREATING COMPUTER OBJECTS FROM DATA SUPPLIED IN PARSED CSV FILE"""

	def __init__(self, row):
		self.SequenceNo,					self.PatternDate,\
		self.Revision,						self.Version,\
		self.InsertDate,					self.String_timestamp,\
		self.ClientType,					self.OperatingSystem,\
		self.ClientVersion,					self.PolicyVersion,\
		self.PolicySerial,					self.PolicyChecksum,\
		self.IPSSerialNO,					self.IPSChecksum,\
		self.HIStatus,						self.HIReason,\
		self.HIDescription,					self.CreationTime,\
		self.Status,						self.String_Lasttimestatuschanged,\
		self.SiteName,						self.AttributeExtension,\
		self.FullName,						self.Email,\
		self.JobTitle,						self.Department,\
		self.EmployeeNumber,				self.EmploymentStatus,\
		self.OfficePhone,					self.MobilePhone,\
		self.HomePhone,						self.AutoProtectOn,\
		self.Infected,						self.WorstDetection,\
		self.String_LastScanTime,			self.String_LastVirusTime,\
		self.AcceptsContentUpdate,			self.AntivirusengineOn,\
		self.DownloadInsightOn,				self.SONAROn,\
		self.TamperProtectionOn,			self.IntrusionPreventionOn,\
		self.IEBrowserProtectionOn,			self.FirefoxBrowserProtectionOn,\
		self.EarlyLaunchAntimalwareOn,		self.MajorVersion,\
		self.MinorVersion,					self.RestartRequired,\
		self.RestartReason,					self.ComputerName,\
		self.ComputerDomainName,			self.Currentlogindomain,\
		self.String_Lastdownloadtime,		self.NumberOfProcessors,\
		self.OperatingSystemLanguage,		self.Totaldiskspace,\
		self.Totalmemory,					self.Computerdescription,\
		self.Servicepack,					self.ProcessorType,\
		self.ProcessorClock,				self.BIOSversion,\
		self.TPMdeviceinstalled,			self.IPAddress1,\
		self.IPAddress2,					self.IPAddress3,\
		self.IPAddress4,					self.Gateway1,\
		self.Gateway2,						self.Gateway3,\
		self.Gateway4,						self.MACAddress1,\
		self.MACAddress2,					self.MACAddress3,\
		self.MACAddress4,					self.DNSserver1,\
		self.DNSserver2,					self.WINSserver1,\
		self.WINSserver2,					self.DHCPserver,\
		self.HardwareKey,					self.Freememory,\
		self.Freediskspace,					self.Timezoneoffset,\
		self.NetworkThreatProtectionOn,		self.ServerName,\
		self.GroupName,						self.DomainName,\
		self.CurrentUser,					self.IPSVersion,\
		self.DeploymentStatus = row

		self.timestamp = 0
		self.last_status_change = 0
		self.last_virus = 0
		self.last_download = 0
		self.last_scan = 0
		self.rev = 0
		self.definition_version = 0

		# CONVERTING DATES TO TIMESTAMPS
		if self.String_timestamp != "Time Stamp":
			self.timestamp = int(MyDate.timestamp_from_date( self.String_timestamp ))
			self.last_status_change = int(MyDate.timestamp_from_date( self.String_Lasttimestatuschanged ))
			self.last_virus = int(MyDate.timestamp_from_date( self.String_LastVirusTime ))
			self.last_download = int(MyDate.timestamp_from_date( self.String_Lastdownloadtime ))
			self.definition_version = int(MyDate.date_to_time( self.Version ))
			if self.String_LastScanTime != "Never":
				self.last_scan = MyDate.timestamp_from_date_mdy( self.String_LastScanTime )
			else:
				self.last_scan = 0
			if self.Revision != "Revision" and self.Revision != "" and self.Revision != " ":
				self.rev = int(self.Revision)

		# AQUIRING CITY NAME FROM HOSTNAME
		self.city = MyCity.get(self.ComputerName)

		# CORRECTIONS
		self.ComputerName = self.ComputerName.upper()
		self.CurrentUser = self.CurrentUser.upper()
		if self.last_virus < 0:
			self.last_virus = 0

	def get_cn(self):
		return self.ComputerName

	@staticmethod
	def check_name(name):
		# CHECKING FOR NAMES THAT SHOULD BE EXCLUDED
		try:
			vdi = name.index("exclude")
			if vdi > -1:
				return 1
		except Exception as ex:
			pass

		# CHECKING FOR NAMES THAT SHOULD BE EXCLUDED
		try:
			vdi = name.index("EXCLUDE")
			if vdi > -1:
				return 1
		except Exception as ex:
			pass

		# REACH THIS FAR - NAME CORRECT
		return 0

class Logo:
	""" DRAWING LOGO ON SCREEN """

	def __init__(self):
		print( """
=========================================================""" + Fore.GREEN +  Style.BRIGHT + """
     ______   __  __     ______     ______               
    /\  == \ /\ \_\ \   /\  == \   /\  __ \\              
    \ \  _-/ \ \____ \  \ \  __<   \ \ \/\ \\             
     \ \_\    \/\_____\  \ \_\ \_\  \ \_____\\            
      \/_/     \/_____/   \/_/ /_/   \/_____/   v.1.1    
                                                         """ + Fore.RESET + Style.NORMAL +"""
=========================================================

 PYRO - SYMANTEC ENDPOINT PROTECTION (SEP) COMPUTERS 
 STATUS EXPORT PARSER, WHICH WILL UPLOAD THE PARSED DATA 
 TO SPECIFIED COUCHDB DATABASE.         """ +  Fore.GREEN + Style.DIM + """by mnmnc @ 2014\
""" + Fore.RESET + Style.NORMAL + "\n")

class MyCouch:
	""" COMMUNICATES WITH COUCHDB SERVER """

	def __init__(self, server, port, user, password, database):
		# ESTABLISHING CONNECTION
		self.server = pycouchdb.Server("http://" + user + ":" + password + "@" + server + ":" + port + "/")
		self.db = self.server.database(database)

	def check_doc_rev(self, doc_id):
		# CHECKS REVISION OF SUPPLIED DOCUMENT
		try:
			rev = self.db.get(doc_id)
			return rev["_rev"]
		except Exception as inst:
			return -1

	def update(self, all_computers):
		# UPDATES DATABASE WITH JSON STRING
		try:
			result = self.db.save_bulk( all_computers, transaction=False )
			sys.stdout.write( " Updating database\t\t\t\t      "+ Fore.GREEN + Style.BRIGHT + u'√' + Fore.RESET + Style.NORMAL + "\t\t" )
			sys.stdout.flush()
			return result
		except Exception as ex:
			sys.stdout.write( " Updating database\t\t\t\t      "+ Fore.RED + Style.BRIGHT + u'¬' + Fore.RESET + Style.NORMAL + "\t\t" )
			sys.stdout.write( "\n Exception: "+ Fore.RED + Style.BRIGHT )
			print( ex )
			sys.stdout.write( Fore.RESET + Style.NORMAL )
			sys.stdout.flush()
			print(" ")
			return None

class Reader:
	""" READING CSV FILE -> LIST """
	def __init__(self, filename):
		self.file = csv.reader(open(filename), delimiter=',', quotechar='"')

	def get_list(self):
		return self.file

class ComputerList:
	""" HOLDS COMPUTERS LIST AND FUNCTIONS 
		REQUIRED FOR GENERATION OF JSON """

	def __init__(self, passed_list):
		self.list = list(map(Computer, passed_list ))

	def get_computer_list(self):
		return self.list

	def get_list_len(self):
		return len(self.list)
	

	def build_dictionary_structure(self):
		# BUILDING JSON STRUCTURE FROM LIST

		self.computers_list = []
		index = 0
		current_char = "-"
		number_of_computers = len(self.list)

		for computer in self.list:

			# PRINTING PROGRESS CHAR
			index = index + 1
			if index%10 == 0:
				sys.stdout.write( " Building JSON structure\t\t\t      "+ Fore.YELLOW + Style.BRIGHT + current_char + Fore.RESET + Style.NORMAL + "\t" + str(index) + " / " + str(number_of_computers) + "\r"  )
				sys.stdout.flush()

				if current_char == "-":
					current_char = "\\"
				elif current_char == "\\":
					current_char = "|"
				elif current_char == "|":
					current_char = "/"
				else:
					current_char = "-"


			# RULLING OUT EXCLUDED NAMES
			name_check = Computer.check_name( computer.ComputerName )

			if computer.ComputerName != "COMPUTER NAME" and name_check == 0  :
				# REVISION CHECK
				rev = couch.check_doc_rev( computer.ComputerName )

				# SPLITTING SPECIFIC FIELDS TO THREE CATHEGORIES
				date = 	{ 															\
					"timestamp": 					computer.timestamp,				\
					"report_date":					today_timestamp,				\
					"last_status_change": 			computer.last_status_change ,	\
					"last_scan": 					computer.last_scan,				\
					"last_virus": 					computer.last_virus,			\
					"last_download": 				computer.last_download			
				}
				
				vir =	{															\
					"revision": 					computer.rev,			\
					"definition_version":			computer.definition_version,	\
					"client_version": 				computer.ClientVersion,	\
					"policy_version": 				computer.PolicyVersion,	\
					"infected": 					computer.Infected,			\
					"worst_detect": 				computer.WorstDetection
				}

				osnet = {															\
					"os" : 							computer.OperatingSystem,		\
					"cn" : 							computer.ComputerName,			\
					"domain" : 						computer.ComputerDomainName,	\
					"current_login_domain" : 		computer.Currentlogindomain, 	\
					"ip": 							computer.IPAddress1,			\
					"free_space":					computer.Freediskspace,			\
					"user":							computer.CurrentUser,			\
					"city":							computer.city
				}
				list_item = {}

				# IF DOCUMENT/COMPUTER EXISTS IN DB, 
				# THIS WILL BE AN UPDATE. _REV REQUIRED
				if rev != -1:
					list_item = { 						\
						"_id": computer.ComputerName, 	\
						"_rev": rev,					\
						"date": date,					\
						"vir":	vir,					\
						"osnet": osnet					\
					}
				# OTHERWISE THIS WILL BE AN ADDITION
				else:
					list_item = { 						\
						"_id": computer.ComputerName,	\
						"date": date,					\
						"vir":	vir,					\
						"osnet": osnet					\
					}
				self.computers_list.append( list_item )

		return self.computers_list

	def pretty_print(self):
		print(json.dumps(self.computers_list, sort_keys=True, indent=4))

class MyJSON:	
	""" CONVERTS LIST TO JSON STRING """
	def list_to_json(self):
		self.json_string
		return json_string

class MyDate:
	""" STATIC METHODS FOR DATE CONVERSIONS """

	@staticmethod
	def date_to_time( date ):
		# 2014-07-07 rev 22 SPLIT TO 2014-07-07 CONVERTED TO TIMESTAMP
		if (len(date) > 9 ):
			to_convert_date, dummy, revision = date.split(" ")
			return time.mktime(datetime.datetime.strptime(to_convert_date, "%Y-%m-%d").timetuple())
		else:
			return 0

	@staticmethod
	def timestamp_from_date( date ):
		if (len(date) > 9 ):
			return int(time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").timetuple()))
		else:
			return 0

	@staticmethod
	def timestamp_from_date_mdy( date ):
		if (len(date) > 9 ):
			return int(time.mktime(datetime.datetime.strptime(date, "%m/%d/%Y %H:%M:%S").timetuple()))
		else:
			return 0

	@staticmethod
	def date_to_revision_number( date ):
		# GETTING REVISION NUMBER FROM 2014-07-07 rev 22
		if (len(date)>9):
			to_convert_date, dummy, revision = date.split(" ")
			int_revision = int(revision.lstrip("0"))
			return int_revision
		else:
			return -1

class MyCity:
	""" CITY CLASSIFICATION BASED ON HOSTNAME """

	@staticmethod
	def get( hostname ):
		# cto		- CITY1
		# ctr		- CITY1
		# cte 		- CITY2
		# cty 		- CITY2
		if (hostname[:3]).lower() == "cto" or (hostname[:3]).lower() == "ctr":
			return "CITY1"
		elif (hostname[:3]).lower() == "cte" or (hostname[:3]).lower() == "cty":
			return "CITY2"
		else:
			return "OTHER"

class Arguments:
	""" CHECKS IF CORRECT ARGUMENTS HAVE BEEN SUPPLIED """

	def __init__(self):
		if len(sys.argv) != 2:
			sys.stdout.write(" Checking arguments\t\t\t\t      " + Fore.RED + Style.BRIGHT + u'¬' + Fore.RESET + Style.NORMAL) 
			sys.stdout.flush()
			print(Fore.RED + "\n Error 0x1: To few arguments.")
			print("\tUsage:")
			print("\t\t./pyro.py filename.csv" + Fore.RESET)
			sys.exit("\n I give up.\n")
		else:
			sys.stdout.write( " Checking arguments\t\t\t\t      "+ Fore.GREEN + Style.BRIGHT + u'√' + Fore.RESET + Style.NORMAL )
			sys.stdout.flush()
			self.filename = sys.argv[1];

	def get_filename(self):
		return self.filename

##### STARTING EXECUTION #####

Logo()

# REQUIRING DATE FOR THE REPORT TIMESTAMP
today = input(" Please provide the date of report\n (YYYY-MM-DD):")
today_timestamp = int(MyDate.timestamp_from_date( today + " 00:00:00" ))

# TURNING OFF THE CURSOR DRAWING FOR ESTHETIC PURPOSES
os.system('setterm -cursor off')

# CHECKING ARGUMENTS COUNT
print("\n Checking arguments \r", end="")
arguments = Arguments()

# CONNECTING ATTEMPT
print("\n Connecting to server \r", end="")
try:
	couch = MyCouch( "1.0.0.2", "7777", "username", "password", "t")
	sys.stdout.write( " Connecting to server\t\t\t\t      "+ Fore.GREEN + Style.BRIGHT + u'√' + Fore.RESET + Style.NORMAL )
	sys.stdout.flush()
except Exception as ex:
	sys.stdout.write(" Connecting to server\t\t\t\t      " + Fore.RED + Style.BRIGHT + u'¬' + Fore.RESET + Style.NORMAL) 
	sys.stdout.flush()
	sys.exit("\n Quitting.")


# PARSING CSV FILE
print("\n Parsing csv file \r", end="")
try:
	reader = Reader( arguments.get_filename() )
except Exception as ex:
	sys.stdout.write( " Parsing csv file\t\t\t\t      "+ Fore.RED + Style.BRIGHT + u'¬' + Fore.RESET + Style.NORMAL )
	sys.stdout.flush()
	print("\n"+ex)
	sys.exit("\n Quitting. Exception while trying to parse the file.")

# IF PARSED SUCCESSFULLY
sys.stdout.write( " Parsing csv file\t\t\t\t      "+ Fore.GREEN + Style.BRIGHT + u'√' + Fore.RESET + Style.NORMAL )
sys.stdout.flush()

# CREATING PROPER LIST OF COMPUTERS
print("\n Creating computers list \r", end="")
try:
	computers = ComputerList(reader.get_list())
except Exception as ex:
	sys.stdout.write( " Creating computers list\t\t\t\t      "+ Fore.RED + Style.BRIGHT + u'¬' + Fore.RESET + Style.NORMAL )
	sys.stdout.flush()
	sys.exit("\n Quitting. Exception while creating a computer list.")

# IF LIST CREATED SUCCESSFULLY
sys.stdout.write( " Creating computers list\t\t\t      "+ Fore.GREEN + Style.BRIGHT + u'√' + Fore.RESET + Style.NORMAL )
sys.stdout.flush()

# DICTIONARY TO JSON STRUCTURE
print("\n Building JSON structure \r", end="")
all_computers = computers.build_dictionary_structure()

sys.stdout.write( " Building JSON structure\t\t\t      "+ Fore.GREEN + Style.BRIGHT + u'√' + Fore.RESET + Style.NORMAL + "            " )
sys.stdout.flush()

# REMOVE COMMENT IF YOU WANT TO SEE THE FULL JSON STRUCTURE BEFORE COMMITTING TO DATABASE
# print("Printing")
# computers.pretty_print()

# UPDATING DATABASE
print("\n Updating database \r", end="")
result = couch.update(all_computers)

# NOTICE. IF YOU WANT TO AVIOD CONFLICTS - REMOVE THE DUPLICATES FROM CSV FILE
print("\n Document update conflicts are acceptible. This might be\n caused by duplicated entries within the update data.")
print("=========================================================")

# TURNING BACK ON THE CURSOR
os.system('setterm -cursor on')

