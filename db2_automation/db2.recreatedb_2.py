#----------------------------------------------------------------------------------------------#
# @author Vincent Tran                                                                         #
# @created Oct 17, 2023                                                                        #
#                                                                                              #
#  PURPOSE:  This program is designed to illustrate how to use the ibm_db.recreatedb() API to  #
#            drop and recreate a database on a remote Db2 server.                              #
#                                                                                              #
#            Additional APIs used:                                                             #
#                 ibm_db.conn_errormsg()                                                       #
#----------------------------------------------------------------------------------------------#

# Load The Appropriate Python Modules
import sys         # Provides Information About Python Interpreter Constants And Functions
import ibm_db      # Contains The APIs Needed To Work With Db2 Databases

#----------------------------------------------------------------------------------------------#
# Import The Db2ConnectionMgr Class Definition, Attributes, And Methods That Have Been Defined #
# In The File Named "ibm_db_tools.py"; This Class Contains The Programming Logic Needed To     #
# Establish And Terminate A Connection To A Db2 Server Or Database                             #
#----------------------------------------------------------------------------------------------#
from ibm_db_tools import Db2ConnectionMgr

#----------------------------------------------------------------------------------------------#
# Import The ipynb_exit Class Definition, Attributes, And Methods That Have Been Defined In    #
# The File Named "ipynb_exit.py"; This Class Contains The Programming Logic Needed To Allow    #
# "exit()" Functionality To Work Without Raising An Error Or Stopping The Kernel If The        #
# Application Is Invoked In A Jupyter Notebook                                                 #
#----------------------------------------------------------------------------------------------#
from ipynb_exit import exit

# Define And Initialize The Appropriate Variables
hostName = "197.126.80.22"    # IP Address Of A Remote Server
portNum = "50000"             # Port Number Used By Db2
userID = "db2inst2"           # User ID (Recognized By The Remote Server)
passWord = "ibmdb2"           # User Password
svrConnection = None
dbName = "MY_DB"
returnCode = False

# Create An Instance Of The Db2ConnectionMgr Class And Use It To Connect To A Remote Db2 Server
conn = Db2ConnectionMgr('SERVER', '', hostName, portNum, userID, passWord)
conn.openConnection()
if conn.returnCode is True:
    svrConnection = conn.connectionID
else:
    conn.closeConnection()
    exit(-1)

# Attempt To Delete (Drop) And Recreate A Database At The Remote Server
print("Dropping and recreating a database named " + dbName + " ", end="")
print("at the " + hostName + " server. Please wait.")
try:
    returnCode = ibm_db.recreatedb(svrConnection, dbName, 'UTF-8')
except Exception:
    pass

# If The Database Could Not Be Recreated, Display An Error Message And Exit 
if returnCode is False:
    print("\nERROR: Unable to drop and recreate the " + dbName + " database.\n")
    errorMsg = ibm_db.conn_errormsg(svrConnection)
    print(errorMsg + "\n")
    conn.closeConnection()
    exit(-1)

# Otherwise, Display A Status Message And Verify That Information About The Database
# That Was Just Recreated Exists In The Db2 System Database Directory
else:
    print("\nThe database \"" + dbName + "\" has been recreated!\n")

# Close The Db2 Server Connection That Was Opened Earlier
conn.closeConnection()

# Return Control To The Operating System
exit()
