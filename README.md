# QnA
A python based command line tool to add new questions, changes to those questions, and display the difference in changes over time for a particular question.  

## What went well
Over all, the coding of python script was enjoyable.

## What was difficult
Setting up a new MySQL server on the resources I had.  I spent a little too much time doing that, and not enough time coding.

## What would I improve if I had more time
I would like to spend a little more time on how/where each word changed in the difference output.

## Dependencies
This script will requires python-MySQLdb library.  To install it on Ubuntu:
`sudo apt-get install python-mysqldb`

This repository comes with the SQL for adding the QnA tables for your MySQL server.  You can add these tables to your MySQL server, like so:

`mysql -u your_username -p QnA < QnA.sql`

You will need to create a MySQL user and password for this script that only have INSERT and SELECT permissions for the QnA tables.  Once you have succesfully logged into your MySQL server, run the following commands;

`CREATE USER 'QnAuser'@'localhost' IDENTIFIED BY 'example_password';
 GRANT INSERT, SELECT PRIVILEGES ON QnA.* TO 'QnAuser'@'localhost';
`
Note: the @localhost will not allow the QnA MySQL user remote access the MySQL server.  This can be changed to accept remote connections, such as '%', however this should be done with caution.  '%' allows connections from anywhere.

## secrets.py

This is where QnA stores the login credentials for the script.  You will need to fill out these variables with the username and  password you supplied in the CREATE USER command above.  For the sake of not commiting login credentials (by accident) to this repo, I have left secrets.py out.  Therefore you will need to create secrets.py in the same directory level as qna.py.  Your secrets.py file should only contain these 2 lines:
`MYSQL_USER   = "QnAuser"
MYSQL_PASSWD = "example_password"
`
## Usage

To add a new question:

`python qna.py -t "Your example question here?"`

To create a change for an existing question"

`python qna.py -t "Your example question here?" -c "Your change to the question here?"`

To display the difference of an existing question through time:

`python qna.py -t "Your example question here?" -d`

For more options:

`python qna.py --help`
