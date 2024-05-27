#----------------------------------------------------------------------------------------------#
# @author Vincent Tran                                                                         #
# @created Oct 17, 2023                                                                        #
#                                                                                              #
#  PURPOSE:  This program is designed to illustrate how to use the ibm_db.stmt_errormsg() API. #
#                                                                                              #
#            Additional APIs used:                                                             #
#                 ibm_db.prepare()                                                             #
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
dbName = "SAMPLE"
userID = "db2inst1"
passWord = "Passw0rd"
dbConnection = None
sqlStatement = " "           # An Empty SQL Statement Is Used To Force An Error To Occur
preparedStmt = False

# Create An Instance Of The Db2ConnectionMgr Class And Use It To Connect To A Db2 Database
conn = Db2ConnectionMgr('DB', dbName, '', '', userID, passWord)
conn.openConnection()
if conn.returnCode is True:
    dbConnection = conn.connectionID
else:
    conn.closeConnection()
    exit(-1)

# Prepare The SQL Statement Specified
print("Preparing the SQL statement specified for execution ... ", end="")
try:
    preparedStmt = ibm_db.prepare(dbConnection, sqlStatement)
except Exception:
    pass

# If Db2 Could Not Parse And Prepare The SQL Statement Correctly, Display An Error Message
# And Exit
if preparedStmt is False:
    print("\nERROR: Unable to prepare the SQL statement specified.")
    errorMsg = ibm_db.stmt_errormsg()
    print("\n" + errorMsg + "\n")
    conn.closeConnection()
    exit(-1)

# Otherwise, Complete The Status Message
else:
    print("Done!\n")

# Close The Database Connection That Was Opened Earlier
conn.closeConnection()

# Return Control To The Operating System
exit()
