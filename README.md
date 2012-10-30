pyTwitterCollector (v 0.1 - October 30, 2012)
=============================================

pyTwitterCollector was originally written by Yazan Hussein (yhussein1@iit.edu) while working for the Collaboration and Social Media Lab at the Illinois Institute of Technology (http://casmlab.org). You can also email the director of the lab, Libby Hemphill (libbyh@gmail.com), with questions.

Planned changes:
- allow Twitter lists instead of files with lists of user_ids
- collect data about followers as well
- add DB schema diagram

Before you start pyTwitterCollector, you need a database to store the tweets. A SQL file for creating the database is included in the repo. 


1) Configuring pyTwitterCollector
---------------------------------

collector.config must be configured prior to starting Collector.py. The configuration file must contain the following:

[db_info] <br />
This section will contain database info. The [db_info] section will contain the following: 
<ol>
<li>host
<li>db_user 
<li>db_pass
</ol>

This is a template of the [db_info] section:<br />
	#this is a comment<br />
	[db_info]<br />
	host = localhost <br />
	db_user = username <br />
	db_pass = password<br />

[user_info]<br />
At least one user section must be defined. The user section must be enclosed in two square brackets. The user section will contain the following:
<ol>
<li>con_key
<li>con_secret 
<li>key
<li>secret
<li>db
<li>include_path
</ol>

This is a template of the user section:<br />
	#This is a comment.<br />
	#you can add as many comments as you want<br />
	#you can define more than one user. A new thread will be created for each user. <br />
	[user_name_goes_here]<br />
	con_key = get con_key from twitter<br />
	con_secret = get con_secret from twitter<br />
	key = get user key from twitter<br />
	secret = get user secret from twitter<br />
	db = database to store tweets. The user defined under [db_info] must have access to the db specified<br />
	include_path = [optional] full path to a file containing twitter ids. If this path is set, then no ids will be retrieved from user account
	
	

2) Starting pyTwitterCollector
------------------------------

Starting Collector.py will load the config file and start collection tweets. A log file will be created in the same directory. This log file will contain info, warnings and errors. Check this file when debugging the collector. The default config file is 'collector.config'. This file must be stored in the same directory as Collector.py or can be set at run rime using:

usage: 

	Collector.py -c path_to_config_file &

