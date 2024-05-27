#----------------------------------------------------------------------------------------------#
# @author Vincent Tran                                                                         #
# @created Oct 17, 2023                                                                        #
#                                                                                              #
#  PURPOSE:  This program is designed to illustrate how to use the ibm_db.primary_keys() API.  #
#                                                                                              #
#            Additional APIs used:                                                             #
#                 ibm_db.fetch_assoc()                                                         #
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
schemaName = userID.upper()
tableName = "PROJECT"
resultSet = False
dataRecord = False

# Create An Instance Of The Db2ConnectionMgr Class And Use It To Connect To A Db2 Database
conn = Db2ConnectionMgr('DB', dbName, '', '', userID, passWord)
conn.openConnection()
if conn.returnCode is True:
    dbConnection = conn.connectionID
else:
    conn.closeConnection()
    exit(-1)

# Attempt To Retrieve Information About All Primary Keys That Have Been Defined For The
# Table Specified
print("Obtaining information about primary keys created for ", end="")
print("the " + schemaName + "." + tableName + " table ... ", end="")
try:
    resultSet = ibm_db.primary_keys(dbConnection, None, schemaName, tableName)
except Exception:
    pass

# If The Information Desired Could Not Be Retrieved, Display An Error Message And Exit
if resultSet is False:
    print("\nERROR: Unable to obtain the information desired\n.")
    conn.closeConnection()
    exit(-1)

# Otherwise, Complete The Status Message
else:
    print("Done!\n")

# As Long As There Are Records (That Were Produced By The ibm_db.primary_keys API), ...
noData = False
loopCounter = 1
while noData is False:

    # Retrieve A Record And Store It In A Python Dictionary
    try:
        dataRecord = ibm_db.fetch_assoc(resultSet)
    except:
        pass

    # If The Data Could Not Be Retrieved Or If There Was No Data To Retrieve, Set The
    # "No Data" Flag And Exit The Loop  
    if dataRecord is False:
        noData = True

    # Otherwise, Display The Information Retrieved
    else:

        # Display Record Header Information
        print("Primary key " + str(loopCounter) + " details:")
        print("______________________________________")

        # Display The Information Stored In The Data Record Retrieved
        print("Primary key table schema  : {}" .format(dataRecord['TABLE_SCHEM']))
        print("Primary key table name    : {}" .format(dataRecord['TABLE_NAME']))
        print("Primary key column name   : {}" .format(dataRecord['COLUMN_NAME']))
        print("Primary key column number : {}" .format(dataRecord['KEY_SEQ']))
        print("Primary key name          : {}" .format(dataRecord['PK_NAME']))

        # Increment The loopCounter Variable And Print A Blank Line To Separate The
        # Records From Each Other
        loopCounter += 1
        print()

# Close The Database Connection That Was Opened Earlier
conn.closeConnection()

# Return Control To The Operating System
exit()
