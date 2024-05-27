#----------------------------------------------------------------------------------------------#
# @author Vincent Tran                                                                         #
# @created Oct 17, 2023                                                                        #
#                                                                                              #
#  PURPOSE:  This program is designed to illustrate how to use the ibm_db.fetch_row() API.     #
#                                                                                              #
#            Additional APIs used:                                                             #
#                 ibm_db.exec_immediate()                                                      #
#                 ibm_db.fetch_row()                                                           #
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
resultSet = False

# Create An Instance Of The Db2ConnectionMgr Class And Use It To Connect To A Db2 Database
conn = Db2ConnectionMgr('DB', dbName, '', '', userID, passWord)
conn.openConnection()
if conn.returnCode is True:
    dbConnection = conn.connectionID
else:
    conn.closeConnection()
    exit(-1)

# Define The SQL Statement That Is To Be Executed
sqlStatement = "SELECT deptname FROM department WHERE admrdept = 'A00'"

# Execute The SQL Statement Just Defined
print("Executing the SQL statement \"" + sqlStatement + "\" ... ", end="")
try:
    resultSet = ibm_db.exec_immediate(dbConnection, sqlStatement)
except Exception:
    pass

# If The SQL Statement Could Not Be Executed, Display An Error Message And Exit 
if resultSet is False:
    print("\nERROR: Unable to execute the SQL statement specified.\n")
    conn.closeConnection()
    exit(-1)

# Otherwise, Complete The Status Message
else:
    print("Done!\n")

# Display A Report Header
print("Query results:\n")
print("DEPTNAME")
print("____________________________")

# As Long As There Are Records In The Result Set Produced, ...
while (ibm_db.fetch_row(resultSet) is True):

    # Display The Data Retrieved
    print(ibm_db.result(resultSet, 0)) 

# Add A Blank Line To The End Of The Report
print()

# Close The Database Connection That Was Opened Earlier
conn.closeConnection()

# Return Control To The Operating System
exit()
