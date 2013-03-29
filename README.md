pyTwitterCollector (v 0.2 - March 28, 2013)
=============================================

pyTwitterCollector was originally written by Yazan Hussein (yhussein1@iit.edu) while working for the Collaboration and Social Media Lab at the Illinois Institute of Technology (http://casmlab.org). You can also email the director of the lab, Libby Hemphill (libbyh@gmail.com), with questions.

Planned changes:
- collect data about followers as well
- update DB schema diagram


Dependencies
------------
pyTwitterCollector was written for Python 2.7. It has not been testing on other versions.

- mysql-python
- tweepy

Setup
-----
Before you start pyTwitterCollector, you need a database to store the tweets. Use TwitterCollector.sql to create it. Make sure you grant permissions on that DB to the user you specify in the config file.
Configuration
---------------------------------

collector.config must be configured prior to starting Collector.py. The configuration file must contain the following:

###DB Info<br />

Template of the [db_info] section:<br />
```python
	#this is a comment
	[db_info]
	host = localhost
	db_user = username
	db_pass = password
```
### User Info<br />
At least one user section must be defined, but you can define more than one.

Template of the user section:<br />
```python
	# This is a comment.
	# You can add as many comments as you want
	# You can define more than one user. A new thread will be created for each user.
	[user_name_goes_here]
	# OAuth settings
	con_key = Consumer key for your Twitter app
	con_secret = Consumer secret for your Twitter app
	key = Access token from your Twitter app
	secret = Access token secret from your Twitter app
	# DB to store the tweets
	db = database to store tweets. The user defined under [db_info] must have access to the db specified
	# Tracking settings
	# By default, pyTwitterCollector tracks the accounts followed by user1. 
	# You may also track Twitter lists or a local list of Twitter IDs
	# To specify Twitter lists, use format owner:slug, owner2:slug2
	lists = None 
	include_path = (optional) full_path

```
	
Usage
--------

Starting Collector.py will load the config file and start collecting tweets. A log file will be created in the same directory. This log file will contain info, warnings and errors. Check this file when debugging the collector. The default config file is 'collector.config'. This file must be stored in the same directory as Collector.py or can be set at run rime using the "-c" option.



	Collector.py -c path_to_config_file &

