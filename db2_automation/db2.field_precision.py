#----------------------------------------------------------------------------------------------#
# @author Vincent Tran                                                                         #
# @created Oct 17, 2023                                                                        #
#                                                                                              #
# PURPOSE:  This program is designed to illustrate how to use the ibm_db.field_precision()     #
#                                                                                              #
#            Additional APIs used:                                                             #
#                 ibm_db.exec_immediate()                                                      #
#                 ibm_db.num_fields()                                                          #
#                 ibm_db.field_name()                                                          #
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
numColumns = False

# Create An Instance Of The Db2ConnectionMgr Class And Use It To Connect To A Db2 Database
conn = Db2ConnectionMgr('DB', dbName, '', '', userID, passWord)
conn.openConnection()
if conn.returnCode is True:
    dbConnection = conn.connectionID
else:
    conn.closeConnection()
    exit(-1)

# Define The SQL Statement That Is To Be Executed
sqlStatement = "SELECT salary, bonus, comm FROM employee"

# Execute The SQL Statement Just Defined
print("Executing the SQL statement \"" + sqlStatement + "\" ... ", end="")
try:
    resultSet = ibm_db.exec_immediate(dbConnection, sqlStatement)
except Exception:
    pass

# If The SQL Statement Could Not Be Executed, Display An Error Message And Exit 
if resultSet is False:
    print("\nERROR: Unable to execute the SQL statement specified.")
    conn.closeConnection()
    exit(-1)

# Otherwise, Complete The Status Message
else:
    print("Done!\n")

# Find Out How Many Columns Were Returned In The Result Set Produced By The Query Just Executed
print("Examining the columns returned in the result set produced ... ", end="")
try:
    numColumns = ibm_db.num_fields(resultSet)
except Exception:
    pass
 
# If Information About The Number Columns Returned Could Not Be Obtained, Display An Error
# Message And Exit 
if numColumns is False:
    print("\nERROR: Unable to obtain information about the result set produced.")
    conn.closeConnection()
    exit(-1)

# Otherwise, Complete The Status Message
else:
    print("Done!\n")

# Display A Report Header
print("Result set information:\n")
print("COLUMN NAME  PRECISION (TOTAL NUMBER OF DIGITS)")
print("___________  __________________________________")

# As Long As There Is Column Information, ...
for loopCounter in range(0, numColumns):

    # Get The Name Of The Current Column
    colName = ibm_db.field_name(resultSet, loopCounter)

    # Get The Precision Of The Current Column
    colPrecision = ibm_db.field_precision(resultSet, loopCounter)

    # Format And Display The Data Retrieved
    if (not colName is False) and (not colPrecision is False):
        print("{:<13}  {:>32}" .format(colName, colPrecision))

# Add A Blank Line To The End Of The Report
print()

# Close The Database Connection That Was Opened Earlier
conn.closeConnection()

# Return Control To The Operating System
exit()
