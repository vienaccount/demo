#----------------------------------------------------------------------------------------------#
# @author Vincent Tran                                                                         #
# @created Oct 17, 2023                                                                        #
#                                                                                              #
#  PURPOSE:  This program is designed to illustrate how to use the ibm_db.rollback() API.      #
#                                                                                              #
#            Additional APIs used:                                                             #
#                 ibm_db.autocommit()                                                          #
#                 ibm_db.exec_immediate()                                                      #
#                 ibm_db.stmt_errormsg()                                                       #
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
# Import The get_row_count() Function That Has Been Defined In The File Named                  #
# "ibm_db_tools.py";  This Function Contains The Programming Logic Needed To Obtain And        #
# Display The Number Of Rows (Records) Found In A Db2 Database Table                           #
#----------------------------------------------------------------------------------------------#
from ibm_db_tools import get_row_count

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
returnCode = False
resultSet = False

# Create An Instance Of The Db2ConnectionMgr Class And Use It To Connect To A Db2 Database
conn = Db2ConnectionMgr('DB', dbName, '', '', userID, passWord)
conn.openConnection()
if conn.returnCode is True:
    dbConnection = conn.connectionID
else:
    conn.closeConnection()
    exit(-1)

# Turn Autocommit Behavior OFF
print("Turning AUTOCOMMIT behavior OFF ... ", end="")
try:
    returnCode = ibm_db.autocommit(dbConnection, ibm_db.SQL_AUTOCOMMIT_OFF)
except Exception:
    pass

# If AUTOCOMMIT Behavior Could Not Be Turned OFF, Display An Error Message And Continue
if returnCode is False:
    print("\nERROR: Unable to turn AUTOCOMMIT behavior OFF.")

# Otherwise, Complete The Status Message
else:
    print("Done!\n")

# Display The Number Of Rows That Currently Exist In The DEPARTMENT Table
returnCode = get_row_count(dbConnection, 'DEPARTMENT')
if returnCode is False:
    conn.closeConnection()
    exit(-1)

# Define The INSERT Statement That Is To Be Used To Add Data To The DEPARTMENT Table
sqlStatement = "INSERT INTO department VALUES('K01', 'SALES', '000130', 'K01', NULL)"

# Execute The SQL Statement Just Defined
print("Inserting a record into the DEPARTMENT table ... ", end="")
try:
    resultSet = ibm_db.exec_immediate(dbConnection, sqlStatement)
except Exception:
    pass

# If The SQL Statement Could Not Be Executed, Display An Error Message And Exit 
if resultSet is False:
    print("\nERROR: Unable to execute the INSERT statement specified.")
    errorMsg = ibm_db.stmt_errormsg()
    print("\n" + errorMsg + "\n")
    conn.closeConnection()
    exit(-1)

# Otherwise, Complete The Status Message
else:
    print("Done!\n")

# Display The Number Of Rows That Exist In The DEPARTMENT Table Now
# (The Number Returned Should Change)
returnCode = get_row_count(dbConnection, 'DEPARTMENT')
if returnCode is False:
    conn.closeConnection()
    exit(-1)

# Back Out The Changes Just Made To The Database
print("Backing out changes made to the database ... ", end="")
resultSet = False
try:
    resultSet = ibm_db.rollback(dbConnection)
except Exception:
    pass

# If The Roll Back Operation Could Not Be Performed, Display An Error Message And Exit 
if resultSet is False:
    print("\nERROR: Unable to roll back the previous operation.")
    conn.closeConnection()
    exit(-1)

# Otherwise, Complete The Status Message
else:
    print("Done!\n")

# Display The Number Of Rows That Exist In The DEPARTMENT Table Now
# (The Number Should Revert Back To The Original Value)
returnCode = get_row_count(dbConnection, 'DEPARTMENT')
if returnCode is False:
    conn.closeConnection()
    exit(-1)

# Close The Database Connection That Was Opened Earlier
conn.closeConnection()

# Return Control To The Operating System
exit()
