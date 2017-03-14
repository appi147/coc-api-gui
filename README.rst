.. highlight:: rst

======================
Clash of Clans API GUI
======================

-----------
Description
-----------

Above program uses API provided by Supercell at https://developer.clashofclans.com/ to perform various operations
It is written in Python 3 and uses tkinter module for creating GUI

--------
Features
--------
* Clan Search By Name
* Clan Search By Tag
* Player Search By Name

--------------------
Features to be added
--------------------

* Get War Log
* Full list of clan search

------------
Shortcomings
------------

* Only top four searches of clan is shown right now
* Full profile of player along with achievements is not shown
* Have to click Refresh Button to load the searches

------
Set Up
------

Since, API uses JSON Web Tokens for authorisation, they have to be manually generated for each user on 
https://developer.clashofclans.com/

For generating token

* Create an account on https://developer.clashofclans.com/
* Find your IP, because JSON Web Token requires IP for authorisation
* Create a token under my account

After token is generated, pre-provided token should be replaced in line 9 of code, under TOKEN variable

------------
Dependencies
------------

Dependencies are tkinter for creating GUI, requests for fetching contents, urllib for encoding URL

Dependencies can be installed as::

	pip3 install requests
	pip3 install urllib3
	apt-get install python3-tk

----------
How to Run
----------

Program can be run::

	python3 coc.py
