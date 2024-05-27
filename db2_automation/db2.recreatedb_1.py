#----------------------------------------------------------------------------------------------#
# @author Vincent Tran                                                                         #
# @created Oct 17, 2023                                                                        #
#                                                                                              #
#  PURPOSE:  This program is designed to illustrate how to use the ibm_db.recreatedb() API to  #
#            drop and recreate a local Db2 database.                                           #
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
userID = "db2inst1"           # User ID (Recognized By The Local Server)
passWord = "Passw0rd"         # User Password
svrConnection = None
dbName = "MY_DB"
returnCode = False

# Create An Instance Of The Db2ConnectionMgr Class And Use It To Connect To The Local Db2 Server
conn = Db2ConnectionMgr('LOCAL_SVR', '', '', '', userID, passWord)
conn.openConnection()
if conn.returnCode is True:
    svrConnection = conn.connectionID
else:
    conn.closeConnection()
    exit(-1)

# Attempt To Drop And Recreate A Database At The Local Server
print("Dropping and recreating a database named " + dbName + ". Please wait.")
try:
    returnCode = ibm_db.recreatedb(svrConnection, dbName, 'UTF-8')
except Exception:
    pass

# If The Database Could Not Be Recreated, Display An Error Message And Exit 
if returnCode is None:
    print("ERROR: Unable to drop and recreate the " + dbName + " database.\n")
    errorMsg = ibm_db.conn_errormsg(svrConnection)
    print(errorMsg + "\n")
    conn.closeConnection()
    exit(-1)
    
# Otherwise, Display A Status Message 
else:
    print("\nThe database \"" + dbName + "\" has been created!\n")
    #    query_sdb_dir(dbName)

# Close The Db2 Server Connection That Was Opened Earlier
conn.closeConnection()

# Return Control To The Operating System
exit()
